import json  
import statistics  
import numpy as np  

# 假设你的 JSONL 文件名为 'data.jsonl'  
filename = '/mnt/tmp/apps/cmss-yangjiandong/staging_stack_v1/analysis/result/data-analysis_stats.jsonl'  
  
alnum_ratios = []  
  
# 读取 JSONL 文件并提取 alnum_ratio 字段  
with open(filename, 'r', encoding='utf-8') as file:  
    for line in file:  
        data = json.loads(line)  
        alnum_ratio = data.get('__dj__stats__').get('word_rep_ratio', None)  
        if alnum_ratio is not None:  
            alnum_ratios.append(alnum_ratio)  
  
# 计算百分位数
percentile_1 = np.percentile(alnum_ratios, 0.5)  
print(f"第0.5百分位数是: {percentile_1}")
percentile_2 = np.percentile(alnum_ratios, 99.5)  
print(f"第99.5百分位数是: {percentile_2}")