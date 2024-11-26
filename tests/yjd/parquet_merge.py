# 筛选指定目录下的.parquet结尾的文件，并将这些文件合并成一个parquet文件

# 使用方法：python3 merge_parquet_files.py <directory> <output_file>

import sys
import os
import pandas as pd

def merge_parquet_files(directory, output_file):

    # 获取指定目录下的所有.parquet文件

    parquet_files = [f for f in os.listdir(directory) if f.endswith('.parquet')]

    # 读取第一个parquet文件并将其存储在一个DataFrame中

    df = pd.read_parquet(os.path.join(directory, parquet_files[0]))

    # 遍历剩余的parquet文件，并将它们追加到DataFrame中

    for f in parquet_files[1:]:

        df_temp = pd.read_parquet(os.path.join(directory, f))

        df = pd.concat([df, df_temp])

    # 将合并后的DataFrame写入新的parquet文件

    df.to_parquet(output_file, index=False)

if __name__ == "__main__":
    dictory = "/mnt/tmp/apps/cmss-yangjiandong/data/the-stack-v2-full-Python/score/the-stack-v2-full-Python-filterscore.parquet/"
    out_file = "/mnt/tmp/apps/cmss-yangjiandong/data/the-stack-v2-full-Python/score/the-stack-v2-full-Python-filterscore-merge.parquet"

    merge_parquet_files(dictory, out_file)
    
