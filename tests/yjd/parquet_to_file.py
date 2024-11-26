# 读取parquet文件的某一列值，生成python文件

# 使用pandas库读取parquet文件
# 使用pandas库的to_csv方法将数据写入csv文件

import pandas as pd
import os

# 读取parquet文件
df = pd.read_parquet('/mnt/tmp/apps/cmss-yangjiandong/data/train/starcoder-python/starcoder-python-score-filter.parquet')

# 选择某一列的值
values = df['text'].values

target_directory = '/mnt/tmp/apps/cmss-yangjiandong/data/starcoder/python'

for index , value in enumerate(values):

    file_name = f'output_{index}.py'
     # 构建文件的完整路径
    file_path = os.path.join(target_directory, file_name)

    with open(file_path, 'w') as f:
        f.write(value)


