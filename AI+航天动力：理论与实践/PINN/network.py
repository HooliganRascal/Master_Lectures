import torch
from torch import nn


class Network(nn.Module):
    """使用指定隐藏层数和激活函数构建全连接网络。"""

    def __init__(
        self,
        input_size: int,
        hidden_size: int,
        output_size: int,
        depth: int,
        act: type[nn.Module] = nn.Tanh,
    ) -> None:
        super().__init__()
        if depth < 1:
            raise ValueError("depth atleast 1")

        layers: list[nn.Module] = []
        for layer_index in range(depth):
            in_features = input_size if layer_index == 0 else hidden_size
            layers.extend([nn.Linear(in_features, hidden_size), act()])

        # 输出层不使用激活函数，允许预测值覆盖正负实数。
        layers.append(nn.Linear(hidden_size, output_size))
        self.layers = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """将形状为 (..., input_size) 的输入映射为 (..., output_size) 的输出。"""
        return self.layers(x)
