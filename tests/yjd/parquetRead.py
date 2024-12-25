import pandas as pd  
  
# 替换为你的Parquet文件路径  
# parquet_file_path = '/workspace/mnt/cmss-liujiahao/ModelLink/dataset/abap/data-00000-of-00001.parquet'
# parquet_file_path = '/root/work/filestorage/cmss-yangjiandong/data/staing-python10/data-00143-of-00144-filter10.parquet'
parquet_file_path='/mnt/tmp/apps/cmss-yangjiandong/data/the-stack-v2-full-java/filter/part1/the-stack-v2-full-java-filter1.parquet'
  
# 读取Parquet文件  
df = pd.read_parquet(parquet_file_path)  
# # 输出parquet文件的列名
# print(df.columns)


# 如果你只想查看第一行  
print(df.iloc[1])


# import pyarrow.parquet as pq  
  
# def count_parquet_rows(file_path):  
#     """  
#     计算 Parquet 文件的总行数。  
  
#     :param file_path: Parquet 文件的路径  
#     :return: 文件的总行数  
#     """  
#     try:  
#         # 打开 Parquet 文件  
#         parquet_file = pq.ParquetFile(file_path)  
#         # 获取文件的元数据  
#         metadata = parquet_file.metadata  
#         # Parquet 文件的行数通常存储在元数据的 num_rows 属性中  
#         # 注意：这个属性可能不准确，特别是如果文件是以追加模式写入的  
#         total_rows = metadata.num_rows  
#         return total_rows  
#     except Exception as e:  
#         print(f"无法读取 Parquet 文件 {file_path}: {e}")  
#         return -1  # 或者你可以选择返回其他表示错误的值  
  
# # 示例使用  
# file_path = '/mnt/tmp/apps/cmss-yangjiandong/ruff/high/data_100.parquet'  
# total_rows = count_parquet_rows(file_path)  
# if total_rows != -1:  
#     print(f"Parquet 文件 {file_path} 的总行数是: {total_rows}")  
# else:  
#     print("无法计算文件的总行数")