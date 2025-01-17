import json  
import statistics  
  
# 假设你的 JSONL 文件名为 'data.jsonl'  
filename = '/mnt/tmp/apps/cmss-yangjiandong/data/stack-v2-c++/analy_stats.jsonl'  
  
alnum_ratios = []  
  
# 读取 JSONL 文件并提取 alnum_ratio 字段  
with open(filename, 'r', encoding='utf-8') as file:  
    for line in file:  
        data = json.loads(line)  
        alnum_ratio = data.get('__dj__stats__', {}).get('max_line_length', None)  
        if alnum_ratio is not None:  
            alnum_ratios.append(alnum_ratio)  
  
# 计算平均值 
mean_alnum_ratio = statistics.mean(alnum_ratios)  
# 计算方差
variance_alnum_ratio = statistics.variance(alnum_ratios)  
# 计算标准差
std_dev_alnum_ratio = statistics.stdev(alnum_ratios)
# 计算最大值
max_value = max(alnum_ratios)  
# 计算最小值
min_value = min(alnum_ratios)
# 计算3-σ区间  
lower_bound = mean_alnum_ratio - 3 * std_dev_alnum_ratio  
upper_bound = mean_alnum_ratio + 3 * std_dev_alnum_ratio 

print(f"最小值: {min_value}")  
print(f"最大值: {max_value}")  
print(f"平均值: {mean_alnum_ratio}")  
print(f"方差: {variance_alnum_ratio}")
print(f"样本标准差: {std_dev_alnum_ratio}")
print(f"3-σ区间: ({lower_bound}, {upper_bound})") 