import os
import re
import torch
import torch.nn as nn

# ------------------------------
# 超参数（需与训练时一致）
# ------------------------------
EMBEDDING_DIM = 100
HIDDEN_DIM = 256
NUM_LAYERS = 2
DROPOUT = 0.5
DEVICE = torch.device('cuda:1' if torch.cuda.is_available() else 'cpu')

# ------------------------------
# tokenizer（与训练时一致）
# ------------------------------
def basic_english_tokenizer(text: str):
    text = text.lower()
    return re.findall(r"\b\w+\b", text)

# ------------------------------
# 词表加载函数
# ------------------------------
def load_vocab(vocab_path):
    """词表保存为 txt，每行 'word index'"""
    vocab = {}
    with open(vocab_path, 'r', encoding='utf8') as f:
        for line in f:
            word, idx = line.strip().split()
            vocab[word] = int(idx)
    return vocab

# ------------------------------
# LSTM 模型定义
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
# 主函数
# ------------------------------
if __name__ == "__main__":
    # 词表路径
    vocab_path = "model/vocab.txt"  # 你的词表文件
    vocab = load_vocab(vocab_path)
    vocab_size = len(vocab)

    # 初始化模型
    model = LSTMClassifier(
        vocab_size, EMBEDDING_DIM, HIDDEN_DIM,
        2, NUM_LAYERS, DROPOUT
    ).to(DEVICE)

    # 加载训练好的模型参数
    model.load_state_dict(torch.load("model/LSTM1.pt", map_location=DEVICE))

    # 测试示例
    example_texts = [
        "I really loved this movie, it was fantastic!",
        "This film was absolutely terrible, I hated it."
    ]

    for text in example_texts:
        sentiment = predict_sentiment(model, vocab, basic_english_tokenizer, text)
        print(f"\nText: {text}")
        print(f"Predicted Sentiment: {sentiment}")
