# 弯曲管道流场训练脚本。B 表示批大小，H/W 表示两个网格方向，C 表示通道。
# 各样本共享结构化网格的索引拓扑，物理 X/Y 坐标描述不同管道的几何形状。
# 模型在规则索引空间做 FFT，再将预测值对应回物理网格进行可视化。
"""
@author: Zongyi Li and Daniel Zhengyu Huang
"""

# F 提供 GELU、补零等函数；plt 用于训练期间的预测结果可视化。
import torch.nn.functional as F
import matplotlib.pyplot as plt
from timeit import default_timer
# 公共工具通过星号导入，还会带入其中的 torch、np、nn 等模块名。
from utilities3 import *
# 使用作者自定义的 Adam；其中复数梯度的二阶矩按 g * conj(g) 累积。
from Adam import Adam

# 固定 PyTorch、NumPy 和 CUDA 随机种子，便于比较重复实验。
# cuDNN 的确定性设置针对其支持的算子，不代表全部硬件上的结果逐位相同。
torch.manual_seed(0)
np.random.seed(0)
torch.cuda.manual_seed(0)
torch.backends.cudnn.deterministic = True

################################################################
# fourier layer
################################################################
# 二维谱卷积：输入 [B,Cin,H,W]，输出 [B,Cout,H,W]。
# 对空间维做 FFT，在选定的低频位置混合通道，再逆变换回空间域。
class SpectralConv2d(nn.Module):
    def __init__(self, in_channels, out_channels, modes1, modes2):
        super(SpectralConv2d, self).__init__()

        """
        2D Fourier layer. It does FFT, linear transform, and Inverse FFT.    
        """

        # in_channels/out_channels 是特征通道数，modes1/modes2 是保留的频率数。
        self.in_channels = in_channels
        self.out_channels = out_channels
        # rfft2 仅压缩最后一个空间维；第一个空间维仍保留正、负频率。
        # 因此第一个方向分别选取频谱开头和末尾的低频区域。
        self.modes1 = modes1  # Number of Fourier modes to multiply, at most floor(N/2) + 1
        self.modes2 = modes2

        # 缩小随机权重的初始化幅度，避免初始谱卷积输出过大。
        self.scale = (1 / (in_channels * out_channels))
        # 权重形状为 [Cin,Cout,modes1,modes2]，每个频率位置有独立的通道混合矩阵。
        # 傅里叶系数是复数，因此可学习权重也使用 torch.cfloat。
        self.weights1 = nn.Parameter(
            self.scale * torch.rand(in_channels, out_channels, self.modes1, self.modes2, dtype=torch.cfloat))
        # 第二组权重用于第一个空间方向的负频率区域，与第一组独立学习。
        self.weights2 = nn.Parameter(
            self.scale * torch.rand(in_channels, out_channels, self.modes1, self.modes2, dtype=torch.cfloat))

    # Complex multiplication
    # einsum 中 i 是输入通道、o 是输出通道，x/y 是频率索引；仅对 i 求和。
    # 不同频率之间不做混合，每个频率分别执行一次复数矩阵乘法。
    def compl_mul2d(self, input, weights):
        # (batch, in_channel, x,y ), (in_channel, out_channel, x,y) -> (batch, out_channel, x,y)
        return torch.einsum("bixy,ioxy->boxy", input, weights)

    def forward(self, x):
        # 此处 x 的布局为 [B,Cin,H,W]，B 为当前批次的样本数。
        batchsize = x.shape[0]
        # Compute Fourier coeffcients up to factor of e^(- something constant)
        # 对最后两个维度做二维实数 FFT，得到 [B,Cin,H,W//2+1] 的复数频谱。
        x_ft = torch.fft.rfft2(x)

        # Multiply relevant Fourier modes
        # 创建输出频谱；未写入的频率保持为零，相当于对这一分支做频率截断。
        out_ft = torch.zeros(batchsize, self.out_channels, x.size(-2), x.size(-1) // 2 + 1, dtype=torch.cfloat,
                             device=x.device)
        # 保留第一个方向开头、第二个方向开头的低频块。
        out_ft[:, :, :self.modes1, :self.modes2] = \
            self.compl_mul2d(x_ft[:, :, :self.modes1, :self.modes2], self.weights1)
        # 第一个方向的负频率位于数组末尾，因此还需写入这个频率块。
        out_ft[:, :, -self.modes1:, :self.modes2] = \
            self.compl_mul2d(x_ft[:, :, -self.modes1:, :self.modes2], self.weights2)

        # Return to physical space
        # 逆 FFT 恢复实数特征场；s 显式指定原尺寸，确保奇数宽度也能正确恢复。
        x = torch.fft.irfft2(out_ft, s=(x.size(-2), x.size(-1)))
        return x


# 整体 FNO：坐标特征提升维度 -> 四层谱卷积/逐点线性分支 -> 标量输出。
# 本脚本实际输入为物理坐标 [X,Y]，并额外拼接计算网格坐标，共 4 个通道。
class FNO2d(nn.Module):
    def __init__(self, modes1, modes2, width):
        super(FNO2d, self).__init__()

        """
        The overall network. It contains 4 layers of the Fourier layer.
        1. Lift the input to the desire channel dimension by self.fc0 .
        2. 4 layers of the integral operators u' = (W + K)(u).
            W defined by self.w; K defined by self.conv .
        3. Project from the channel space to the output space by self.fc1 and self.fc2 .

        input: the solution of the coefficient function and locations (a(x, y), x, y)
        input shape: (batchsize, x=s, y=s, c=3)
        output: the solution 
        output shape: (batchsize, x=s, y=s, c=1)
        """

        self.modes1 = modes1
        self.modes2 = modes2
        self.width = width
        # 在空间维补 8 个零，为 FFT 的周期延拓留出缓冲，输出前再裁去。
        self.padding = 8  # pad the domain if input is non-periodic
        # 这里实际接收 [X,Y,xi,eta] 四个通道；原英文模板中的 3 通道说明
        # 不对应本脚本的数据。Linear 作用于最后一维，输出 width 维特征。
        self.fc0 = nn.Linear(4, self.width)  # input channel is 3: (a(x, y), x, y)

        # 四个谱卷积分支在频域建模全局空间关系。
        self.conv0 = SpectralConv2d(self.width, self.width, self.modes1, self.modes2)
        self.conv1 = SpectralConv2d(self.width, self.width, self.modes1, self.modes2)
        self.conv2 = SpectralConv2d(self.width, self.width, self.modes1, self.modes2)
        self.conv3 = SpectralConv2d(self.width, self.width, self.modes1, self.modes2)
        # 1×1 卷积只混合当前位置的通道，对应公式中的局部线性分支 W。
        self.w0 = nn.Conv2d(self.width, self.width, 1)
        self.w1 = nn.Conv2d(self.width, self.width, 1)
        self.w2 = nn.Conv2d(self.width, self.width, 1)
        self.w3 = nn.Conv2d(self.width, self.width, 1)

        # 输出投影逐点执行 width -> 128 -> 1，得到每个网格点的一个标量。
        self.fc1 = nn.Linear(self.width, 128)
        self.fc2 = nn.Linear(128, 1)

    def forward(self, x):
        # 输入 x 为 [B,H,W,2]，其中两个通道分别是该样本的物理 X/Y 坐标。
        grid = self.get_grid(x.shape, x.device)
        # grid 是规则计算网格坐标 [xi,eta]；拼接后 x 变为 [B,H,W,4]。
        x = torch.cat((x, grid), dim=-1)
        # 提升通道数：[B,H,W,4] -> [B,H,W,width]。
        x = self.fc0(x)
        # 调整为卷积使用的布局 [B,width,H,W]；permute 仅改变维度顺序。
        x = x.permute(0, 3, 1, 2)

        # F.pad 的参数顺序是 [W左,W右,H上,H下]，这里仅在两个方向的末端补零。
        x = F.pad(x, [0, self.padding, 0, self.padding])

        # 第一层：谱分支 K(x) 负责全局关系，逐点分支 W(x) 补充局部通道变换。
        x1 = self.conv0(x)
        x2 = self.w0(x)
        # 两个分支形状一致，逐元素相加后通过 GELU 引入非线性。
        x = x1 + x2
        x = F.gelu(x)

        # 第二层继续对上一层特征执行同样的 K(x) + W(x) 结构。
        x1 = self.conv1(x)
        x2 = self.w1(x)
        x = x1 + x2
        x = F.gelu(x)

        # 第三层谱卷积与逐点线性变换。
        x1 = self.conv2(x)
        x2 = self.w2(x)
        x = x1 + x2
        x = F.gelu(x)

        # 第四层相加后不立即使用 GELU，随后进入输出投影。
        x1 = self.conv3(x)
        x2 = self.w3(x)
        x = x1 + x2

        # 裁掉补零部分，恢复原来的 H/W；随后将通道维移回最后一维。
        x = x[..., :-self.padding, :-self.padding]
        x = x.permute(0, 2, 3, 1)
        # 逐网格点执行两层全连接映射，最终输出形状为 [B,H,W,1]。
        x = self.fc1(x)
        x = F.gelu(x)
        x = self.fc2(x)
        return x

    # 生成与物理坐标不同的计算坐标：沿两个网格索引方向均匀覆盖 [0,1]。
    def get_grid(self, shape, device):
        batchsize, size_x, size_y = shape[0], shape[1], shape[2]
        gridx = torch.tensor(np.linspace(0, 1, size_x), dtype=torch.float)
        # 把一维 xi 扩展到所有样本和所有列，形状为 [B,H,W,1]。
        gridx = gridx.reshape(1, size_x, 1, 1).repeat([batchsize, 1, size_y, 1])
        gridy = torch.tensor(np.linspace(0, 1, size_y), dtype=torch.float)
        # 把一维 eta 扩展到所有样本和所有行，形状同样为 [B,H,W,1]。
        gridy = gridy.reshape(1, 1, size_y, 1).repeat([batchsize, size_x, 1, 1])
        # 拼接为 [B,H,W,2]，并移动到与输入相同的设备。
        return torch.cat((gridx, gridy), dim=-1).to(device)


################################################################
# configs
################################################################
# 原始数据路径相对于程序启动时的工作目录解析。
INPUT_X = './pipe/Pipe_X.npy'
INPUT_Y = './pipe/Pipe_Y.npy'
OUTPUT_Sigma = './pipe/Pipe_Q.npy'

# 仅使用前 N=1200 个样本，其中前 1000 个训练，最后 200 个测试。
ntrain = 1000
ntest = 200
N = 1200

# 每批 20 个样本，初始学习率为 0.001。
batch_size = 20
learning_rate = 0.001

# 训练 501 轮；每完成 100 轮，学习率乘以 0.5。
epochs = 501
step_size = 100
gamma = 0.5

# 两个网格方向各使用 modes=12 个模态；隐藏特征通道数为 width=32。
modes = 12
width = 32

# r1/r2 是网格下采样步长；s1/s2 根据原始 129×129 网格计算保留尺寸。
r1 = 1
r2 = 1
s1 = int(((129 - 1) / r1) + 1)
s2 = int(((129 - 1) / r2) + 1)

################################################################
# load data and data normalization
################################################################
# 读取各样本的物理坐标并转换为 float32。
# 虽然上方英文标题提到 normalization，这段实际没有执行归一化。
inputX = np.load(INPUT_X)
inputX = torch.tensor(inputX, dtype=torch.float)
inputY = np.load(INPUT_Y)
inputY = torch.tensor(inputY, dtype=torch.float)
# 把 X/Y 堆叠到最后一维，得到 [N,H,W,2] 的几何输入。
input = torch.stack([inputX, inputY], dim=-1)

# Q 的布局按 [N,C,H,W] 使用，[:,0] 选择第 1 个输出通道。
# 通道的具体物理含义取决于数据集定义；此处模型只预测这一标量场。
output = np.load(OUTPUT_Sigma)[:, 0]
output = torch.tensor(output, dtype=torch.float)

# 先限定前 N 个样本，再划分训练/测试集，并对两个空间维下采样。
# 在默认 ntrain=1000、ntest=200、N=1200 的配置下，两组样本不重叠。
x_train = input[:N][:ntrain, ::r1, ::r2][:, :s1, :s2]
y_train = output[:N][:ntrain, ::r1, ::r2][:, :s1, :s2]
x_test = input[:N][-ntest:, ::r1, ::r2][:, :s1, :s2]
y_test = output[:N][-ntest:, ::r1, ::r2][:, :s1, :s2]
# 输入整理为 [样本数,s1,s2,2]，目标 y 的形状为 [样本数,s1,s2]。
x_train = x_train.reshape(ntrain, s1, s2, 2)
x_test = x_test.reshape(ntest, s1, s2, 2)

# 坐标网格和参考场组成样本对；训练集每轮打乱，测试集保持顺序。
train_loader = torch.utils.data.DataLoader(torch.utils.data.TensorDataset(x_train, y_train), batch_size=batch_size,
                                           shuffle=True)
test_loader = torch.utils.data.DataLoader(torch.utils.data.TensorDataset(x_test, y_test), batch_size=batch_size,
                                          shuffle=False)
# 另建 batch_size=1 的测试加载器；本文件后续训练循环未使用它。
test_loader2 = torch.utils.data.DataLoader(torch.utils.data.TensorDataset(x_test, y_test), batch_size=1,
                                          shuffle=False)

################################################################
# training and evaluation
################################################################
# 管道实验两个方向使用相同的 modes；原代码将模型放到 CUDA 上。
model = FNO2d(modes, modes, width).cuda()
# 按张量元素数统计参数；一个复数元素在 count_params 中计为一个。
print(count_params(model))

# 使用作者的 Adam 更新参数；weight_decay 是加入梯度的 L2 惩罚。
optimizer = Adam(model.parameters(), lr=learning_rate, weight_decay=1e-4)
# StepLR 根据已经完成的 epoch 数调节学习率。
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=step_size, gamma=gamma)

# 默认调用相对 L2 损失；size_average=False 表示先对 batch 内样本求和。
myloss = LpLoss(size_average=False)

# 每轮依次执行训练、学习率更新、测试和可选绘图。
for ep in range(epochs):
    # 切换到训练模式，并统计本轮累计损失和耗时。
    model.train()
    t1 = default_timer()
    train_l2 = 0
    for x, y in train_loader:
        # 把输入和参考场移动到 GPU，与模型处于相同设备。
        x, y = x.cuda(), y.cuda()

        # 清空上一批次的梯度，避免不同 batch 的梯度累积。
        optimizer.zero_grad()
        # 前向传播得到 [B,s1,s2,1] 的预测。
        out = model(x)

        # 分别展平成 [batch_size,网格点数]，按样本计算 ||预测-参考||₂ / ||参考||₂。
        # 这里按固定 batch_size 展平；默认样本数均可被 20 整除。
        loss = myloss(out.view(batch_size, -1), y.view(batch_size, -1))
        # 反向传播损失，自动计算所有可训练参数的梯度。
        loss.backward()

        # 更新参数；item() 将损失取为 Python 标量，用于累计而不保留计算图。
        optimizer.step()
        train_l2 += loss.item()

    # 一个 epoch 更新一次学习率，调用次序位于参数更新之后。
    scheduler.step()

    # 切换到评估模式，测试阶段只计算误差，不进行反向传播。
    model.eval()
    test_l2 = 0.0
    # no_grad 关闭梯度记录，减少测试阶段的内存开销。
    with torch.no_grad():
        for x, y in test_loader:
            x, y = x.cuda(), y.cuda()

            out = model(x)

            # 每个测试 batch 返回逐样本相对误差之和，随后累计到 test_l2。
            test_l2 += myloss(out.view(batch_size, -1), y.view(batch_size, -1)).item()

    # 累计误差分别除以训练和测试样本数，得到平均相对 L2 误差。
    train_l2 /= ntrain
    test_l2 /= ntest

    t2 = default_timer()
    # 依次打印 epoch、耗时、训练平均误差、测试平均误差。
    print(ep, t2 - t1, train_l2, test_l2)

    # ep 从 0 开始，因此第 0、100、200...轮绘图；模型保存语句保持注释状态。
    if ep%step_size==0:
        # torch.save(model, '../model/pipe_' + str(ep))
        # 使用最后一个测试 batch 的第一个样本；在其物理 X/Y 坐标上绘图。
        # detach 脱离计算图，cpu 移到主机，numpy 转为绘图数组。
        X = x[0, :, :, 0].squeeze().detach().cpu().numpy()
        Y = x[0, :, :, 1].squeeze().detach().cpu().numpy()
        truth = y[0].squeeze().detach().cpu().numpy()
        pred = out[0].squeeze().detach().cpu().numpy()

        # 三行依次显示参考场、预测场和带符号误差 pred-truth。
        fig, ax = plt.subplots(nrows=3, figsize=(16, 16))
        ax[0].pcolormesh(X, Y, truth, shading='gouraud')
        ax[1].pcolormesh(X, Y, pred, shading='gouraud')
        ax[2].pcolormesh(X, Y, pred-truth, shading='gouraud')
        # 显示图形；这段原代码没有将图片保存到文件。
        fig.savefig("pipe.png")


