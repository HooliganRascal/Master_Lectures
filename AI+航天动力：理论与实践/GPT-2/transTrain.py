import torch
from datasets import load_from_disk
# datasets 是 Hugging Face 提供的处理数据集的工具。load_from_disk 可以从本地加载离线数据集
# 如果不使用load_from_disk，程序在第一次运行时会从Hugging Face网站下载数据集，但因网络原因，通常会失败
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
from transformers import DataCollatorForLanguageModeling
# transformers是训练、微调、推理、部署预训练大模型的API，封装了模型、分词器、训练循环、数据集接口
# 几乎支持所有的开源的预训练模型，如GPT，BERT，deepseek等，只要开源了模型权重、配置、分词器，就可使用

# 1. 加载数据集 ==========
dataset = load_from_disk("./hf_offline_assets/wikitext-2")
print("Dataset loaded:", dataset)

# 2. 加载分词器和模型 ==========
tokenizer = GPT2Tokenizer.from_pretrained("./hf_offline_assets/gpt2_tokenizer")
model = GPT2LMHeadModel.from_pretrained("./hf_offline_assets/gpt2_model")

# 
tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = model.config.eos_token_id

# 3. 数据分词 ==========
def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=128)

tokenized_datasets = dataset.map(tokenize_function, batched=True, remove_columns=["text"])
# Hugging Face的map方法：为datasets中的每一条数据，应用一个相同的函数进行操作，这里就是调用了tokenizer
print("Tokenized dataset example:", tokenized_datasets["train"][0])

# ========== 4. DataCollator：语言模型的动态mask（这里是因果语言建模） ==========
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# 5. 训练参数 ==========
training_args = TrainingArguments(
    output_dir="./gpt2_finetuned_wikitext2",
    overwrite_output_dir=True,
    num_train_epochs=1,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    save_strategy="epoch",
    logging_dir="./logs",
    logging_steps=50,
    learning_rate=5e-5,
    fp16=torch.cuda.is_available(),
    report_to="none",  # 不连接wandb等外部日志系统
)

# 6. Trainer ==========
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    data_collator=data_collator,
)

# 7. 开始训练 ==========
trainer.train()

# 8. 保存模型 ==========
save_path = "./gpt2_finetuned_wikitext2_final"
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)

print(f"模型已保存到：{save_path}")
