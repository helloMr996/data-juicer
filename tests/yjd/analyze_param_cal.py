import json  
import statistics  
import numpy as np  

# 假设你的 JSONL 文件名为 'data.jsonl'  
filename = '/mnt/tmp/apps/cmss-yangjiandong/data/stack-v2-c++/analy_stats.jsonl'  
  
alnum_ratios = []  
alpha_token_ratios =[]
avg_line_lengths=[]
char_rep_ratios=[]
max_line_lengths=[]
num_wordss=[]
text_lens=[]
word_rep_ratios=[]
  
# 读取 JSONL 文件并提取 alnum_ratio 字段  
with open(filename, 'r', encoding='utf-8') as file:  
    for line in file:  
        data = json.loads(line) 
         
        alnum_ratio = data.get('__dj__stats__').get('alnum_ratio', None)  
        if alnum_ratio is not None:  
            alnum_ratios.append(alnum_ratio)

        alpha_token_ratio = data.get('__dj__stats__').get('alpha_token_ratio', None)  
        if alpha_token_ratio is not None:  
            alpha_token_ratios.append(alpha_token_ratio)  
        
        avg_line_length = data.get('__dj__stats__').get('avg_line_length', None)  
        if avg_line_length is not None:  
            avg_line_lengths.append(avg_line_length)  
        
        char_rep_ratio = data.get('__dj__stats__').get('char_rep_ratio', None)  
        if char_rep_ratio is not None:  
            char_rep_ratios.append(char_rep_ratio)  

        max_line_length = data.get('__dj__stats__').get('max_line_length', None)  
        if max_line_length is not None:  
            max_line_lengths.append(max_line_length) 


        num_words = data.get('__dj__stats__').get('num_words', None)  
        if num_words is not None:  
            num_wordss.append(num_words) 

        text_len = data.get('__dj__stats__').get('text_len', None)  
        if text_len is not None:  
            text_lens.append(text_len) 
        
        word_rep_ratio = data.get('__dj__stats__').get('word_rep_ratio', None)  
        if word_rep_ratio is not None:  
            word_rep_ratios.append(word_rep_ratio) 


values = [alnum_ratios, alpha_token_ratios, avg_line_lengths, char_rep_ratios, max_line_lengths, num_wordss, text_lens, word_rep_ratios]
indexName = ['alnum_ratios', 'alpha_token_ratios', 'avg_line_lengths', 'char_rep_ratios', 'max_line_lengths', 'num_wordss', 'text_lens', 'word_rep_ratios']
for index,value in enumerate(values): 
    # 计算百分位数
    name = indexName[index]
    print(f"====================={name}===============")
    percentile_1 = np.percentile(value, 0.5)  
    percentile_2 = np.percentile(value, 99.5)  
    print(f"第0.5百分位数是: {percentile_1}, 第99.5百分位数是: {percentile_2}")
    # 计算平均值 
    mean_alnum_ratio = statistics.mean(value)  
    # 计算方差
    variance_alnum_ratio = statistics.variance(value)  
    # 计算标准差
    std_dev_alnum_ratio = statistics.stdev(value)
    # 计算最大值
    max_value = max(value)  
    # 计算最小值
    min_value = min(value)
    # 计算3-σ区间  
    lower_bound = mean_alnum_ratio - 3 * std_dev_alnum_ratio  
    upper_bound = mean_alnum_ratio + 3 * std_dev_alnum_ratio 
    print(f"最小值: {min_value}")  
    print(f"最大值: {max_value}")  
    print(f"平均值: {mean_alnum_ratio}")  
    print(f"方差: {variance_alnum_ratio}")
    print(f"样本标准差: {std_dev_alnum_ratio}")
    print(f"3-σ区间: ({lower_bound}, {upper_bound})") 