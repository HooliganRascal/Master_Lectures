import os, time, re
from collections import Counter

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence


start_time = time.time()

# ------------------------------
# 超参数
# ------------------------------
BATCH_SIZE = 16
MAX_SEQ_LEN = 500
EMBEDDING_DIM = 100
HIDDEN_DIM = 256
NUM_LAYERS = 2
DROPOUT = 0.5
EPOCHS = 20
LR = 0.001
DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


# ------------------------------
# tokenizer（代替 torchtext）
# ------------------------------
def basic_english_tokenizer(text: str):
    text = text.lower()
    return re.findall(r"\b\w+\b", text)


# ------------------------------
# 构建词表（代替 torchtext.vocab）
# ------------------------------
def build_vocab(data_dir, tokenizer, min_freq=2):
    counter = Counter()

    for label in ['pos', 'neg']:
        folder = os.path.join(data_dir, label)
        for file in os.listdir(folder):
            path = os.path.join(folder, file)
            with open(path, "r", encoding="utf8") as f:
                tokens = tokenizer(f.read())
                counter.update(tokens)

    vocab = {"<unk>": 0}
    for word, freq in counter.items():
        if freq >= min_freq:
            vocab[word] = len(vocab)

    return vocab


# ------------------------------
# Dataset
# ------------------------------
class IMDBDataset(Dataset):
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
                    tokens = tokenizer(f.read())[:MAX_SEQ_LEN]
                    indexed = [vocab.get(t, self.unk) for t in tokens]
                    self.samples.append((indexed, 1 if label == 'pos' else 0))

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

vocab_save_path = "model/vocab.txt"
os.makedirs(os.path.dirname(vocab_save_path), exist_ok=True)
with open(vocab_save_path, "w", encoding="utf8") as f:
    for word, idx in vocab.items():
        f.write(f"{word} {idx}\n")
print(f"词表已保存到 {vocab_save_path}")

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
        embedded = self.dropout(self.embedding(text))  # (seq_len, batch, embed_dim)
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

criterion = nn.CrossEntropyLoss()
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

        optimizer.zero_grad(set_to_none=True)
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
    tokens = tokenizer(text)[:MAX_SEQ_LEN]
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
