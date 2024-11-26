# 提取某一个parquet文件的前100行，生成新的parquet文件


import pandas as pd
import pyarrow.parquet as pq

# 读取parquet文件
df = pq.read_table('/mnt/tmp/apps/cmss-yangjiandong/staging_stack_v1/scoreresult/the-stack-v2-full-Python-filterscoreTmpSplit_1.parquet').to_pandas()

# 提取前100行
df_100 = df.head(10000)

# 写入新的parquet文件
df_100.to_parquet('/mnt/tmp/apps/cmss-yangjiandong/ruff/high/data_10000.parquet')
