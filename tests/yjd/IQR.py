import json  
import statistics  
import numpy as np  

# 假设你的 JSONL 文件名为 'data.jsonl'  
filename = '/mnt/tmp/apps/cmss-yangjiandong/data-juicer/outputs/demo-analyzer/demo-analyzer-result_stats.jsonl'  
  
alnum_ratios = []  
  
# 读取 JSONL 文件并提取 alnum_ratio 字段  
with open(filename, 'r', encoding='utf-8') as file:  
    for line in file:  
        data = json.loads(line)  
        alnum_ratio = data.get('__dj__stats__', {}).get('text_len', None)  
        if alnum_ratio is not None:  
            alnum_ratios.append(alnum_ratio)  
  
# 计算第一四分位数（Q1）和第三四分位数（Q3）  
Q1 = np.percentile(alnum_ratios, 25)  
Q3 = np.percentile(alnum_ratios, 75)  
  
# 计算IQR  
IQR = Q3 - Q1  
  
# 设定异常值的阈值，通常使用1.5倍或3倍的IQR  
lower_bound = Q1 - 1.5 * IQR  
upper_bound = Q3 + 1.5 * IQR  
  
# 识别异常值  
# outliers = [x for x in alnum_ratios if x < lower_bound or x > upper_bound]  
  
print(f"第一四分位数（Q1）: {Q1}")  
print(f"第三四分位数（Q3）: {Q3}")  
print(f"IQR: {IQR}")  
print(f"异常值阈值（下界）: {lower_bound}")  
print(f"异常值阈值（上界）: {upper_bound}")  
# print(f"异常值: {outliers}")


asd = None