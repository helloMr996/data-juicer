# 困惑度过滤
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import math

# 加载预训练的GPT-2模型和分词器
model_name = 'gpt2'
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# 准备测试集文本
test_texts = [
    "I am a student. I go to school everyday cause I like every of my classmates and teachers",
    "Mike is a software engineer,he programs on working days. he has very high skill to produce good quality software!",
    "haha, I adrt gqsf fgwf  dgwa wuklala.",
    "The quick brown fox jumps over a lazy dog, the dog didn't take any actions."
]

def calculate_perplexity(model, tokenizer, text):
    model.eval()
    inputs = tokenizer(text, return_tensors='pt')
    with torch.no_grad():
        outputs = model(**inputs, labels=inputs['input_ids'])
        loss = outputs.loss
        perplexity = torch.exp(loss)
    return perplexity.item()

# 设置困惑度阈值
perplexity_threshold = 200

filtered_texts = []
for text in test_texts:
    ppl = calculate_perplexity(model, tokenizer, text)
    if ppl < perplexity_threshold:
        filtered_texts.append((text, ppl))
    print(f"Text: {text}, Perplexity: {ppl}")

print("\nFiltered Texts:")
for text, ppl in filtered_texts:
    print(f"Text: {text}, Perplexity: {ppl}")