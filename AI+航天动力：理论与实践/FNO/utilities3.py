# Geo-FNO 公共工具：数据读取、归一化、Lp 损失、辅助网络和分布距离。
# 除特别说明外，张量第一维 N/B 表示样本，其余维度表示空间、时间或通道。
# 归一化统计量应由训练集估计，再用于测试集；导入模块本身不会执行归一化。
import torch
import numpy as np
import scipy.io
import h5py
import torch.nn as nn

# operator.mul 与 reduce 用于最后的参数维度连乘统计。
import operator
from functools import reduce
#################################################
#
# Utilities
#
#################################################
# 根据 CUDA 可用性提供默认设备变量；本变量不会自动移动模型或数据。
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# reading data
# 统一读取传统 MAT、MATLAB v7.3 MAT 和普通 HDF5 文件。
class MatReader(object):
    # to_torch 控制是否转为 Tensor，to_cuda 控制 Tensor 是否转到 GPU，
    # to_float 控制是否将读取的数组转换为 float32。
    def __init__(self, file_path, to_torch=True, to_cuda=False, to_float=True):
        super(MatReader, self).__init__()

        self.to_torch = to_torch
        self.to_cuda = to_cuda
        self.to_float = to_float

        self.file_path = file_path

        # data 保存变量字典或 HDF5 文件对象；两个标志区分不同读取方式。
        self.data = None
        self.old_mat = True
        self.h5 = False
        self._load_file()

    def _load_file(self):

        # 普通 .h5 文件直接交给 h5py，数据以 Dataset 形式保存。
        if self.file_path[-3:] == '.h5':
            self.data = h5py.File(self.file_path, 'r')
            self.h5 = True

        else:
            try:
                # 传统 MAT 文件由 scipy.io.loadmat 读取，结果可按变量名索引。
                self.data = scipy.io.loadmat(self.file_path)
            except:
                # 若 scipy 读取失败，尝试 HDF5 路径，以兼容 MATLAB v7.3。
                self.data = h5py.File(self.file_path, 'r')
                self.old_mat = False

    # 修改文件路径并重新加载；格式标志的更新方式保持原实现。
    def load_file(self, file_path):
        self.file_path = file_path
        self._load_file()

    # field 是文件中的变量名，例如 input/output；返回一个字段的数据。
    def read_field(self, field):
        x = self.data[field]

        if self.h5:
            # [()] 将 HDF5 Dataset 的内容读入内存中的 NumPy 数组。
            x = x[()]

        # 按 HDF5 方式读取的 MAT 文件需要反转轴顺序，以恢复 MATLAB 变量的布局。
        # 普通 .h5 分支不会执行这一步轴反转。
        if not self.old_mat:
            x = x[()]
            x = np.transpose(x, axes=range(len(x.shape) - 1, -1, -1))

        # 默认转为实数单精度，以匹配本项目训练数据和模型的常用精度。
        if self.to_float:
            x = x.astype(np.float32)

        if self.to_torch:
            # NumPy 数组转换为 PyTorch Tensor；GPU 转移只在 to_torch=True 时执行。
            x = torch.from_numpy(x)

            if self.to_cuda:
                x = x.cuda()

        return x

    # 这三个 setter 只修改后续读取的配置，不会转换此前返回的数组。
    def set_cuda(self, to_cuda):
        self.to_cuda = to_cuda

    def set_torch(self, to_torch):
        self.to_torch = to_torch

    def set_float(self, to_float):
        self.to_float = to_float

# normalization, pointwise gaussian
# 逐位置标准化：每个空间点/特征分别统计训练样本的均值和标准差。
# 例如 x=[N,H,W]，沿 N 维统计后 mean/std 均为 [H,W]。
class UnitGaussianNormalizer(object):
    def __init__(self, x, eps=0.00001):
        super(UnitGaussianNormalizer, self).__init__()

        # x could be in shape of ntrain*n or ntrain*T*n or ntrain*n*T
        # 只沿第 0 维统计；后续 encode/decode 利用广播支持不同大小的 batch。
        self.mean = torch.mean(x, 0)
        self.std = torch.std(x, 0)
        # eps 加到标准差上，避免零标准差导致直接除零。
        self.eps = eps

    # 标准化公式 z=(x-mean)/(std+eps)，不改变输入的维度布局。
    def encode(self, x):
        x = (x - self.mean) / (self.std + self.eps)
        return x

    # 反标准化公式 x=z*(std+eps)+mean；sample_idx 可指定仅恢复部分位置。
    def decode(self, x, sample_idx=None):
        if sample_idx is None:
            std = self.std + self.eps # n
            mean = self.mean
        else:
            # 保留原代码对索引形状的判断：此分支直接在统计量上按 sample_idx 取值。
            if len(self.mean.shape) == len(sample_idx[0].shape):
                std = self.std[sample_idx] + self.eps  # batch*n
                mean = self.mean[sample_idx]
            # 此分支保留统计量的第一个维度，再按 sample_idx 选择后续位置；
            # 调用时的索引格式和数据布局需要与该分支一致。
            if len(self.mean.shape) > len(sample_idx[0].shape):
                std = self.std[:,sample_idx]+ self.eps # T*batch*n
                mean = self.mean[:,sample_idx]

        # x is in shape of batch*n or T*batch*n
        x = (x * std) + mean
        return x

    # 归一化器不是 nn.Module，统计量需单独移动；这里原地更新 mean/std 属性。
    def cuda(self):
        self.mean = self.mean.cuda()
        self.std = self.std.cuda()

    # 将统计量移回 CPU；与 cuda() 一样，此方法没有显式返回新对象。
    def cpu(self):
        self.mean = self.mean.cpu()
        self.std = self.std.cpu()

# normalization, Gaussian
# 全局标准化：整个张量共用一个均值和一个标准差，区别于逐位置统计。
# 这种变换只调整位置和尺度，并不保证原始分布变为高斯分布。
class GaussianNormalizer(object):
    def __init__(self, x, eps=0.00001):
        super(GaussianNormalizer, self).__init__()

        # 没有指定 dim，因此对全部样本、空间位置和通道一起求统计量。
        self.mean = torch.mean(x)
        self.std = torch.std(x)
        self.eps = eps

    # 用同一组全局统计量对训练或测试数据编码。
    def encode(self, x):
        x = (x - self.mean) / (self.std + self.eps)
        return x

    # 恢复原始物理量；这里保留 sample_idx 参数，但实现中并未使用它。
    def decode(self, x, sample_idx=None):
        x = (x * (self.std + self.eps)) + self.mean
        return x

    # 将全局统计量移到 GPU；待处理张量也需要在同一设备。
    def cuda(self):
        self.mean = self.mean.cuda()
        self.std = self.std.cuda()

    # 将全局统计量移回 CPU。
    def cpu(self):
        self.mean = self.mean.cpu()
        self.std = self.std.cpu()


# normalization, scaling by range
# 逐特征 min-max 缩放：把训练集各位置的最小值映射到 low，最大值映射到 high。
class RangeNormalizer(object):
    def __init__(self, x, low=0.0, high=1.0):
        super(RangeNormalizer, self).__init__()
        # 沿样本维取最小/最大值，随后展平特征维；每个特征分别确定缩放系数。
        mymin = torch.min(x, 0)[0].view(-1)
        mymax = torch.max(x, 0)[0].view(-1)

        # 构造仿射变换 z=a*x+b；此处沿用原式，未对最大值等于最小值的情况加保护。
        self.a = (high - low)/(mymax - mymin)
        self.b = -self.a*mymax + high

    def encode(self, x):
        # 先记住原形状，再保留 batch 维展平，便于与一维的 a/b 做广播计算。
        s = x.size()
        x = x.view(s[0], -1)
        x = self.a*x + self.b
        # 把缩放后的特征恢复到输入的原始形状。
        x = x.view(s)
        return x

    # 使用 x=(z-b)/a 反向恢复物理量，展平和还原规则与 encode 相同。
    def decode(self, x):
        s = x.size()
        x = x.view(s[0], -1)
        x = (x - self.b)/self.a
        x = x.view(s)
        return x

#loss function with rel/abs Lp loss
# 按样本计算绝对/相对 Lp 误差；p=2 时对应 L2 范数，而不是 MSE。
# 默认调用 __call__ 会转入 rel，相对误差的参考量是第二个参数 y。
class LpLoss(object):
    def __init__(self, d=2, p=2, size_average=True, reduction=True):
        super(LpLoss, self).__init__()

        #Dimension and Lp-norm type are postive
        assert d > 0 and p > 0

        # d 是绝对误差积分近似的空间维度，p 是范数阶数。
        # reduction=False 返回逐样本误差；否则由 size_average 决定求均值还是求和。
        self.d = d
        self.p = p
        self.reduction = reduction
        self.size_average = size_average

    # 绝对 Lp 误差：用网格间距权重 h^(d/p) 将离散范数近似为连续范数。
    def abs(self, x, y):
        num_examples = x.size()[0]

        #Assume uniform mesh
        # 假设单位区间上的均匀网格，并由第一个空间方向计算 h。
        # 这一简化不包含非均匀曲线网格的单元面积或 Jacobian 权重。
        h = 1.0 / (x.size()[1] - 1.0)

        # 展平非 batch 维，对每个样本单独计算差值的 p 范数，结果形状为 [B]。
        all_norms = (h**(self.d/self.p))*torch.norm(x.reshape(num_examples,-1) - y.reshape(num_examples,-1), self.p, 1)

        # 按配置将 [B] 的逐样本误差求均值或求和；关闭 reduction 则直接返回数组。
        if self.reduction:
            if self.size_average:
                return torch.mean(all_norms)
            else:
                return torch.sum(all_norms)

        return all_norms

    # 相对 Lp 误差：先对每个样本求 ||x-y||p 和 ||y||p，再逐样本相除。
    def rel(self, x, y):
        num_examples = x.size()[0]

        # reshape 仅保留 batch 维，其余空间、时间或通道元素全部合并。
        diff_norms = torch.norm(x.reshape(num_examples,-1) - y.reshape(num_examples,-1), self.p, 1)
        y_norms = torch.norm(y.reshape(num_examples,-1), self.p, 1)

        # 这里先计算逐样本的相对误差，再汇总；不是把两个 batch 范数直接相除。
        # 原代码的分母没有 epsilon 保护，零参考场的处理方式也保持原样。
        if self.reduction:
            if self.size_average:
                return torch.mean(diff_norms/y_norms)
            else:
                return torch.sum(diff_norms/y_norms)

        return diff_norms/y_norms

    # 使实例可像函数一样调用：myloss(pred,target) 默认计算相对误差。
    def __call__(self, x, y):
        return self.rel(x, y)

# A simple feedforward neural network
# 普通多层感知机 MLP，与图像分类中具有密集连接结构的 DenseNet 不是同一网络。
class DenseNet(torch.nn.Module):
    # layers 给出各层宽度，如 [2,64,1]；nonlinearity 传激活函数类，如 nn.ReLU。
    # normalize 控制隐藏层的 BatchNorm1d，out_nonlinearity 控制最后的输出激活。
    def __init__(self, layers, nonlinearity, out_nonlinearity=None, normalize=False):
        super(DenseNet, self).__init__()

        # 相邻两个宽度定义一层 Linear，因此线性层数量等于宽度列表长度减一。
        self.n_layers = len(layers) - 1

        assert self.n_layers >= 1

        # ModuleList 注册各个子层，使参数能被优化器、state_dict 和设备迁移机制管理。
        self.layers = nn.ModuleList()

        for j in range(self.n_layers):
            self.layers.append(nn.Linear(layers[j], layers[j+1]))

            # 隐藏层按 Linear -> 可选 BatchNorm -> 激活排列；最后一个 Linear 默认不接激活。
            if j != self.n_layers - 1:
                if normalize:
                    self.layers.append(nn.BatchNorm1d(layers[j+1]))

                self.layers.append(nonlinearity())

        # 如果显式提供输出激活，则追加在整个网络末尾。
        if out_nonlinearity is not None:
            self.layers.append(out_nonlinearity())

    # 按注册顺序逐层计算输出，保留原来的模块组织方式。
    def forward(self, x):
        for _, l in enumerate(self.layers):
            x = l(x)

        return x

# 计算两组实数样本的两两距离：输入 [n1,d]、[n2,d]，输出 [n1,n2]。
# 以返回语句为准，结果是含 eps 平滑的距离，而非英文首句所说的距离平方。
def pdist(sample_1, sample_2, norm=2, eps=1e-5):
    r"""Compute the matrix of all squared pairwise distances.
    Arguments
    ---------
    sample_1 : torch.Tensor or Variable
        The first sample, should be of shape ``(n_1, d)``.
    sample_2 : torch.Tensor or Variable
        The second sample, should be of shape ``(n_2, d)``.
    norm : float
        The l_p norm to be used.
    Returns
    -------
    torch.Tensor or Variable
        Matrix of shape (n_1, n_2). The [i, j]-th entry is equal to
        ``|| sample_1[i, :] - sample_2[j, :] ||_p``."""
    n_1, n_2 = sample_1.size(0), sample_2.size(0)
    norm = float(norm)
    # 欧氏距离使用 ||a-b||²=||a||²+||b||²-2a·b，避免显式创建三维差值数组。
    if norm == 2.:
        norms_1 = torch.sum(sample_1**2, dim=1, keepdim=True)
        norms_2 = torch.sum(sample_2**2, dim=1, keepdim=True)
        norms = (norms_1.expand(n_1, n_2) +
                 norms_2.transpose(0, 1).expand(n_1, n_2))
        distances_squared = norms - 2 * sample_1.mm(sample_2.t())
        # abs 处理舍入产生的负值，再加 eps 开平方；同一点的距离因此约为 sqrt(eps)。
        return torch.sqrt(eps + torch.abs(distances_squared))
    else:
        # 其他 p 值通过广播形成 [n1,n2,d] 的两两差，再沿特征维求 p 范数。
        dim = sample_1.size(1)
        expanded_1 = sample_1.unsqueeze(1).expand(n_1, n_2, dim)
        expanded_2 = sample_2.unsqueeze(0).expand(n_1, n_2, dim)
        differences = torch.abs(expanded_1 - expanded_2) ** norm
        inner = torch.sum(differences, dim=2, keepdim=False)
        return (eps + inner) ** (1. / norm)

# 最大均值差异 MMD 的平方统计量，用于比较两组样本的分布。
# 采用多个高斯核的和；两组内部排除自身配对，有限样本估计可以为负。
# 当前翼型和管道训练脚本没有调用该工具。
class MMDStatistic:
    r"""The *unbiased* MMD test of :cite:`gretton2012kernel`.
    The kernel used is equal to:
    .. math ::
        k(x, x') = \sum_{j=1}^k e^{-\alpha_j\|x - x'\|^2},
    for the :math:`\alpha_j` proved in :py:meth:`~.MMDStatistic.__call__`.
    Arguments
    ---------
    n_1: int
        The number of points in the first sample.
    n_2: int
        The number of points in the second sample."""

    # n_1/n_2 固定两组样本数量；下方分母要求每组至少有两个样本。
    def __init__(self, n_1, n_2):
        self.n_1 = n_1
        self.n_2 = n_2

        # The three constants used in the test.
        # 分别对应组内均值项和跨组均值项的归一化系数。
        self.a00 = 1. / (n_1 * (n_1 - 1))
        self.a11 = 1. / (n_2 * (n_2 - 1))
        self.a01 = - 1. / (n_1 * n_2)

    def __call__(self, sample_1, sample_2, alphas, ret_matrix=False):
        r"""Evaluate the statistic.
        The kernel used is
        .. math::
            k(x, x') = \sum_{j=1}^k e^{-\alpha_j \|x - x'\|^2},
        for the provided ``alphas``.
        Arguments
        ---------
        sample_1: :class:`torch:torch.autograd.Variable`
            The first sample, of size ``(n_1, d)``.
        sample_2: variable of shape (n_2, d)
            The second sample, of size ``(n_2, d)``.
        alphas : list of :class:`float`
            The kernel parameters.
        ret_matrix: bool
            If set, the call with also return a second variable.
            This variable can be then used to compute a p-value using
            :py:meth:`~.MMDStatistic.pval`.
        Returns
        -------
        :class:`float`
            The test statistic.
        :class:`torch:torch.autograd.Variable`
            Returned only if ``ret_matrix`` was set to true."""
        # 把两组样本拼接后一次计算完整距离矩阵，包含组内和跨组距离。
        sample_12 = torch.cat((sample_1, sample_2), 0)
        distances = pdist(sample_12, sample_12, norm=2)

        kernels = None
        # alphas 控制高斯核的尺度；对各尺度 exp(-alpha*距离²) 相加。
        for alpha in alphas:
            kernels_a = torch.exp(- alpha * distances ** 2)
            if kernels is None:
                kernels = kernels_a
            else:
                kernels = kernels + kernels_a

        # 将完整核矩阵拆为第一组内部、第二组内部和跨组的三个子矩阵。
        k_1 = kernels[:self.n_1, :self.n_1]
        k_2 = kernels[self.n_1:, self.n_1:]
        k_12 = kernels[:self.n_1, self.n_1:]

        # MMD² = 第一组组内核均值 + 第二组组内核均值 - 2×跨组核均值。
        # 组内减去 trace，去掉每个样本与自身的配对。
        mmd = (2 * self.a01 * k_12.sum() +
               self.a00 * (k_1.sum() - torch.trace(k_1)) +
               self.a11 * (k_2.sum() - torch.trace(k_2)))
        # ret_matrix=True 时额外返回完整核矩阵；此类本身没有实现 pval 方法。
        if ret_matrix:
            return mmd, kernels
        else:
            return mmd

# print the number of parameters
# 按每个注册参数张量的维度连乘并求和；包含冻结参数，不包含 buffer。
# 沿用原统计口径：一个复数元素计为一个参数，若比较实数自由度则应计为两个。
def count_params(model):
    c = 0
    for p in list(model.parameters()):
        c += reduce(operator.mul, list(p.size()))
    return c
