import json  
import statistics  
import numpy as np  

# 假设你的 JSONL 文件名为 'data.jsonl'  
filename = '/mnt/tmp/apps/cmss-yangjiandong/data/ruff/analyze/data_10000_result_stats.jsonl'  
  
alnum_ratios = []  
  
# 读取 JSONL 文件并提取 alnum_ratio 字段  
with open(filename, 'r', encoding='utf-8') as file:  
    for line in file:  
        data = json.loads(line)  
        alnum_ratio = data.get('__dj__stats__').get('ruff_EF_ratio', None) 

        if alnum_ratio is not None:  
            alnum_ratios.append(alnum_ratio['E-TLOC'] + alnum_ratio['F-TLOC'] )  
  
# 计算百分位数
for i in range(5, 101, 5):
    # 计算第i个百分位数
    percentile = np.percentile(alnum_ratios, i)  
    print(f"第{i}百分位数是: {percentile}")