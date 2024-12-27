import numpy as np  
from scipy.stats import boxcox, norm  
from scipy.special import inv_boxcox   
import json  
# 假设你的 JSONL 文件名为 'data.jsonl'  
filename = '/mnt/tmp/apps/cmss-yangjiandong/data-juicer/outputs/demo-analyzer/demo-analyzer-result_stats.jsonl'  
dataT = []  
# 读取 JSONL 文件并提取 alnum_ratio 字段  
with open(filename, 'r', encoding='utf-8') as file:  
    for line in file:  
        datatmp = json.loads(line)  
        alnum_ratio = datatmp.get('__dj__stats__', {}).get('max_line_length', None)  
        if alnum_ratio is not None:  
            dataT.append(alnum_ratio)  
data = np.array(dataT) 
# 应用 Box-Cox 变换，获取变换后的数据和 λ 值  
data_transformed, lmbda = boxcox(data)  
# 计算变换后数据的均值和标准差  
mean_transformed = np.mean(data_transformed)  
std_transformed = np.std(data_transformed, ddof=1)  
# 计算变换后数据的 3-σ 界限  
lower_bound_transformed = mean_transformed - 3 * std_transformed  
upper_bound_transformed = mean_transformed + 3 * std_transformed  
# 使用 inv_boxcox 逆变换回原始数据的尺度  
lower_bound_original = inv_boxcox(lower_bound_transformed, lmbda)  #测试
upper_bound_original = inv_boxcox(upper_bound_transformed, lmbda)  
# 打印结果   
print("变换后的数据均值和标准差:", mean_transformed, std_transformed)  
print("3-σ 界限（变换后）:", lower_bound_transformed, upper_bound_transformed)  
print("3-σ 界限（逆变换回原始数据）:", lower_bound_original, upper_bound_original)