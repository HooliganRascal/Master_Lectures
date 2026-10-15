# opt3, 数据增强
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import random
def set_seed(seed):
   random.seed(seed)
   torch.manual_seed(seed)
   torch.cuda.manual_seed(seed)
   torch.cuda.manual_seed_all(seed)
   torch.backends.cudnn.deterministic = True
   torch.backends.cudnn.benchmark = False
# set_seed(20)

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
])

transform_aug = transforms.Compose([
    transforms.RandomCrop(32, padding=4),  # 裁剪
    transforms.RandomHorizontalFlip(p=0.5),  # 翻转
    transforms.RandomRotation(15),  # 旋转
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
])


testset = torchvision.datasets.CIFAR10(root='data', train=False, download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=128, shuffle=True)
criterion = nn.CrossEntropyLoss()
trainset_aug = torchvision.datasets.CIFAR10(root='data', train=True, download=True, transform=transform_aug)
trainloader_aug = torch.utils.data.DataLoader(trainset_aug, batch_size=128, shuffle=True)

class CNN_BN_Dropout(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3,16,3,padding=1)
        self.bn1 = nn.BatchNorm2d(16)
        self.conv2 = nn.Conv2d(16,32,3,padding=1)
        self.bn2 = nn.BatchNorm2d(32)
        self.conv3 = nn.Conv2d(32,64,3,padding=1)
        self.bn3 = nn.BatchNorm2d(64)
        self.pool = nn.MaxPool2d(2,2)
        self.dropout = nn.Dropout(0.5)
        self.fc1 = nn.Linear(64*4*4,512)      
        self.fc2 = nn.Linear(512,10)
        self.relu = nn.ReLU()
    def forward(self,x):
        x = self.pool(self.relu(self.bn1(self.conv1(x))))
        x = self.pool(self.relu(self.bn2(self.conv2(x))))
        x = self.pool(self.relu(self.bn3(self.conv3(x))))
        x = x.view(x.size(0),-1)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        return x

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = CNN_BN_Dropout().to(device)
optimizer = optim.AdamW(model.parameters(), lr=0.001)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.5)

model = CNN_BN_Dropout().to(device)
model.load_state_dict(torch.load('./model/model_opt3.pt', map_location=device))
model.eval()

classes = ['plane', 'car', 'bird', 'cat', 'deer',
           'dog', 'frog', 'horse', 'ship', 'truck']

import matplotlib.pyplot as plt
import numpy as np

# 取一个 batch
dataiter = iter(testloader)
images, labels = next(dataiter)

# 如果使用 GPU，需要转回 CPU 才能显示
images_cpu = images[:10].cpu()
labels_cpu = labels[:10].cpu()

# 推理
with torch.no_grad():
    outputs = model(images.to(device))
    _, predicted = torch.max(outputs, 1)

mean = torch.tensor([0.4914, 0.4822, 0.4465]).view(3,1,1)
std = torch.tensor([0.2023, 0.1994, 0.2010]).view(3,1,1)

def imshow(img):
    img = img * std + mean   # 反归一化
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.axis('off')

imshow(torchvision.utils.make_grid(images_cpu))
print('真实标签:', ' '.join('%5s' % classes[labels_cpu[j]] for j in range(10)))
print('预测标签:', ' '.join('%5s' % classes[predicted.cpu()[j]] for j in range(10)))
plt.show()
