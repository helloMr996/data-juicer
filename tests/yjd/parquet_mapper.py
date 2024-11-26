import pandas as pd

# 读取parquet文件
df = pd.read_parquet('/mnt/tmp/apps/cmss-yangjiandong/staging_stack_v1/scoreresult/the-stack-v2-full-Python-filterscore.parquet')

# 提取某一列，并将其转换为一个新的DataFrame
df_column = df[['text']]  # 注意这里使用了双括号，以保留DataFrame结构

# 写入新的parquet文件
df_column.to_parquet('/mnt/tmp/apps/cmss-yangjiandong/staging_stack_v1/scoreresult/the-stack-v2-full-Python-filterscoreTmp.parquet')