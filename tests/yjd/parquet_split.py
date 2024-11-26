# 将一个大parquet文件，按照每900万行切分，切分成多个小parquet文件

import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa

def split_large_parquet(input_file, output_prefix, rows_per_file=9000000):
    # 读取 Parquet 文件
    table = pq.read_table(input_file)
    
    # 获取表的总行数
    num_rows = table.num_rows
    
    # 计算需要的文件数量
    num_files = (num_rows + rows_per_file - 1) // rows_per_file
    
    for i in range(num_files):
        start_row = i * rows_per_file
        end_row = min((i + 1) * rows_per_file, num_rows)
        
        # 提取指定行范围的数据
        chunk = table.slice(start_row, end_row - start_row)
        
        # 将 PyArrow Table 转换为 Pandas DataFrame（可选）
        df = chunk.to_pandas()
        
        # 保存到新的 Parquet 文件
        output_file = f"{output_prefix}_{i+1}.parquet"
        pq.write_table(chunk, output_file)
        print(f"Saved {output_file} with {end_row - start_row} rows")

# 使用示例
input_file = '/mnt/tmp/apps/cmss-yangjiandong/staging_stack_v1/scoreresult/the-stack-v2-full-Python-filterscoreTmp.parquet'  # 输入的大 Parquet 文件路径
output_prefix = '/mnt/tmp/apps/cmss-yangjiandong/staging_stack_v1/scoreresult/the-stack-v2-full-Python-filterscoreTmpSplit'       # 输出文件的前缀
split_large_parquet(input_file, output_prefix)