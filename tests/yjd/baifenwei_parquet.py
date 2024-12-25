#读取parquet文件，获取doc_score字段，并计算百分位数


import pandas as pd
import pyarrow.parquet as pq
import numpy as np

#读取parquet文件
table = pq.read_table('/mnt/tmp/apps/cmss-yangjiandong/data/the-stack-v2-full-c++-pipleline/score/the-stack-v2-c++-nosyntax-score.parquet/part-00044-5a6900d8-ed7d-44ca-90ef-25077fd95c3a-c000.snappy.parquet')
df = table.to_pandas()

#获取doc_score字段
doc_score = df['doc_score']

#计算百分位数
# 计算百分位数
for i in range(5, 101, 5):
    # 计算第i个百分位数
    percentile = np.percentile(doc_score, i)  
    print(f"第{i}百分位数是: {percentile}")



# import os
# import pandas as pd
# import numpy as np

# def read_parquet_files_from_directory(directory):
#     all_texts = []
#     for filename in os.listdir(directory):
#         if filename.endswith(".parquet"):
#             file_path = os.path.join(directory, filename)
#             df = pd.read_parquet(file_path)
#             if 'text' in df.columns:
#                 all_texts.extend(df['text'].dropna().tolist())  # Drop any NaN values
#     return all_texts

# def main():
#     directory = '/mnt/tmp/apps/cmss-yangjiandong/data/the-stack-v2-full-java/score/part1/the-stack-v2-full-java-score1.parquet'  # Replace with your directory path
#     all_texts = read_parquet_files_from_directory(directory)
#     for i in range(5, 101, 5):
#         # 计算第i个百分位数
#         percentile = np.percentile(all_texts, i)  
#         print(f"第{i}百分位数是: {percentile}")

# if __name__ == "__main__":
#     main()
