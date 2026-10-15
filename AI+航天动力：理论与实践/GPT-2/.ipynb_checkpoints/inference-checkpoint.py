import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel


tokenizer = GPT2Tokenizer.from_pretrained("./gpt2_finetuned_wikitext2_final")
model = GPT2LMHeadModel.from_pretrained("./gpt2_finetuned_wikitext2_final")
model.eval()

inputs = tokenizer("Deep learning is", return_tensors="pt")
# outputs = model.generate(**inputs, max_length=30)
outputs = model.generate(**inputs, max_length=30, temperature=0.9, top_k=50)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
