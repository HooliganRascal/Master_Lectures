import os, time, re
from collections import Counter
# Counter是计数器，用来统计每一个单词出现的频率，用于构建词表
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence
# pad_sequence用于把长序列补齐

start_time = time.time()

# ------------------------------
# 定义一些训练用的超参数，比如网络层数、学习率，batch的大小等等
# 通常来说，全文都会使用的变量，以及一些广为人知的常量，如PI=3.141592653等，会使用大写字母
# ------------------------------
BATCH_SIZE = 16
EMBEDDING_DIM = 100
HIDDEN_DIM = 256
NUM_LAYERS = 2
DROPOUT = 0.5
EPOCHS = 20
LR = 0.001
# 使用GPU来训练模型
DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


# ------------------------------
# tokenizer（代替 torchtext）
# ------------------------------
def basic_english_tokenizer(text: str):
    text = text.lower()
    # text.lower()：把文本变小写，归一化（"The" 与 "the" 视为同一词）。
    return re.findall(r"\b\w+\b", text)


# ------------------------------
# 构建词表（代替 torchtext.vocab）
# ------------------------------
def build_vocab(data_dir, tokenizer, min_freq=2):
    counter = Counter()
    # 初始化一个计数器
    for label in ['pos', 'neg']: # 遍历数据集文件夹
        folder = os.path.join(data_dir, label)
        for file in os.listdir(folder):
            path = os.path.join(folder, file)
            with open(path, "r", encoding="utf8") as f:
                tokens = tokenizer(f.read())
                counter.update(tokens)

    vocab = {"<unk>": 0} # vocab = {"<unk>": 0}：初始化词表，<unk> 对应索引 0，用于未登录词（unknown）
    for word, freq in counter.items(): # counter由两部分组成，一个word，一个freq
        if freq >= min_freq:
            vocab[word] = len(vocab)

    return vocab


# ------------------------------
# Dataset
# ------------------------------
class IMDBDataset(Dataset): # 基于Dataset这个类来构建数据集
    def __init__(self, data_dir, vocab, tokenizer):
        self.samples = []
        self.vocab = vocab
        self.tokenizer = tokenizer
        self.unk = vocab["<unk>"]

        for label in ['pos', 'neg']:
            folder = os.path.join(data_dir, label)
            for file in os.listdir(folder):
                path = os.path.join(folder, file)
                with open(path, "r", encoding="utf8") as f:
                    tokens = tokenizer(f.read())
                    indexed = [vocab.get(t, self.unk) for t in tokens] # 把数据集中，每一句话的每一个词转换为索引
                    self.samples.append((indexed, 1 if label == 'pos' else 0)) # 用索引值来代替一句话，如果是pos就为1，如果是neg就为0

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        text, label = self.samples[idx]
        return torch.tensor(text, dtype=torch.long), torch.tensor(label, dtype=torch.long)


# ------------------------------
# collate_fn
# ------------------------------
def collate_fn(batch):
    text_batch, label_batch = zip(*batch)
    # 因为 LSTM batch_first=False → (seq_len, batch)
    text_batch = pad_sequence(text_batch, padding_value=0)
    label_batch = torch.stack(label_batch)
    return text_batch, label_batch


# ------------------------------
# 构建词表
# ------------------------------
tokenizer = basic_english_tokenizer
train_dir = "aclImdb/train"
vocab = build_vocab(train_dir, tokenizer)
vocab_size = len(vocab)

print(f"构建词表完成，词表大小: {vocab_size}")

# ------------------------------
# 数据集与 DataLoader
# ------------------------------
train_dataset = IMDBDataset("aclImdb/train", vocab, tokenizer)
test_dataset = IMDBDataset("aclImdb/test", vocab, tokenizer)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate_fn)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, collate_fn=collate_fn)


# ------------------------------
# LSTM 分类模型
# ------------------------------
class LSTMClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, output_dim, num_layers, dropout):
        """
        vocab_size: 词表的大小
        embed_dim: 词向量的维度
        hidden_dim: 隐藏层维度，神经元数量
        output_dim: LSTM输出维度, 这里是判断语言感情, pos为1, neg为0, 所以是2
        num_layers: 网络设置多少层
        dropout: 防止网络过拟合的方法, 在训练过程中, 随机锁定一部分神经元
        """
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(
            embed_dim,
            hidden_dim,
            num_layers=num_layers,
            dropout=dropout,
            bidirectional=True,
            batch_first=False
        )
        self.fc = nn.Linear(hidden_dim * 2, output_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, text):
        x = self.embedding(text)
        embedded = self.dropout(x)  # (seq_len, batch, embed_dim)
        output, (hidden, cell) = self.lstm(embedded)
        # 双向 LSTM → hidden[-2] 正向最后一层，hidden[-1] 反向最后一层
        hidden_cat = torch.cat((hidden[-2], hidden[-1]), dim=1)
        return self.fc(hidden_cat)


# ------------------------------
# 初始化模型
# ------------------------------
model = LSTMClassifier(
    vocab_size, EMBEDDING_DIM, HIDDEN_DIM,
    2, NUM_LAYERS, DROPOUT
).to(DEVICE)

criterion = nn.CrossEntropyLoss()  # 交叉熵损失函数
optimizer = optim.Adam(model.parameters(), lr=LR)


# ------------------------------
# 训练与评估
# ------------------------------
def train(model, loader, optimizer, criterion):
    model.train()
    total_loss = 0
    total_correct = 0

    for text, labels in loader:
        text, labels = text.to(DEVICE), labels.to(DEVICE)

        optimizer.zero_grad()
        output = model(text)
        loss = criterion(output, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        total_correct += (output.argmax(1) == labels).sum().item()

    return total_loss / len(loader), total_correct / len(loader.dataset)


def evaluate(model, loader, criterion):
    model.eval()
    total_loss = 0
    total_correct = 0

    with torch.no_grad():
        for text, labels in loader:
            text, labels = text.to(DEVICE), labels.to(DEVICE)
            output = model(text)
            loss = criterion(output, labels)

            total_loss += loss.item()
            total_correct += (output.argmax(1) == labels).sum().item()

    return total_loss / len(loader), total_correct / len(loader.dataset)


# ------------------------------
# 训练循环
# ------------------------------
for epoch in range(EPOCHS):
    tr_loss, tr_acc = train(model, train_loader, optimizer, criterion)
    te_loss, te_acc = evaluate(model, test_loader, criterion)
    print(f"Epoch {epoch+1}/{EPOCHS}")
    print(f"Train Loss: {tr_loss:.4f} | Train Acc: {tr_acc:.4f}")
    print(f"Test  Loss: {te_loss:.4f} | Test  Acc: {te_acc:.4f}")
    print("-----------------------------------")

torch.save(model.state_dict(), 'model/LSTM1.pt')
# ------------------------------
# 推理函数
# ------------------------------
def predict_sentiment(model, vocab, tokenizer, text):
    model.eval()
    tokens = tokenizer(text)
    indexed = [vocab.get(t, vocab["<unk>"]) for t in tokens]
    text_tensor = torch.tensor(indexed, dtype=torch.long).unsqueeze(1).to(DEVICE)

    with torch.no_grad():
        output = model(text_tensor)
        pred = output.argmax(1).item()

    return "Positive" if pred == 1 else "Negative"


# ------------------------------
# 测试两个示例
# ------------------------------
example_texts = [
    "I really loved this movie, it was fantastic!",
    "This film was absolutely terrible, I hated it.",
    "This character is so poorly acted.",
    "I think this movie is recommendable."
]

for text in example_texts:
    sentiment = predict_sentiment(model, vocab, tokenizer, text)
    print(f"\nText: {text}")
    print(f"Predicted Sentiment: {sentiment}")

end_time = time.time()
h, rem = divmod(end_time - start_time, 3600)
m, s = divmod(rem, 60)
print(f"\n代码执行时间: {int(h)}小时 {int(m)}分钟 {int(s)}秒")
