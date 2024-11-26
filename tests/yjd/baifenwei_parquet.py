#读取parquet文件，获取doc_score字段，并计算百分位数


import pandas as pd
import pyarrow.parquet as pq
import numpy as np

#读取parquet文件
table = pq.read_table('/mnt/tmp/apps/cmss-yangjiandong/staging_stack_v1/score/staging-stack-v1-python-score.parquet/part-00156-44dc10e7-2bf3-45ab-9255-034fdb80c37b-c000.snappy.parquet')
df = table.to_pandas()

#获取doc_score字段
doc_score = df['doc_score']

#计算百分位数
# 计算百分位数
for i in range(5, 101, 5):
    # 计算第i个百分位数
    percentile = np.percentile(doc_score, i)  
    print(f"第{i}百分位数是: {percentile}")
