import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import io
import json

# Parquet文件路径
input_parquet_file = '/mnt/tmp/apps/cmss-yangjiandong/staging_stack_v1/scoreresult/the-stack-v2-full-Python-filterscoreTmp.parquet'

# 读取Parquet文件到DataFrame
df = pd.read_parquet(input_parquet_file)

# 初始化合并字符串和字节大小计数器
merged_text = ""
merged_text_size = 0

# 将字符串填写到JSON模板中
json_string = ''

# 遍历DataFrame的每一行
for index, row in df.iterrows():
    # 获取text列的值，并将其转换为字符串（以防万一它是其他类型）
    text_value = str(row['text'])
    
    # 计算添加新文本后的总大小（以字节为单位）
    new_text_size = len(text_value.encode('utf-8'))
    
    # 检查是否超过256KB限制
    if merged_text_size > 1048576:  # MB

        filled_json = {
            "text": merged_text
        }
        json_string += json.dumps(filled_json) + '\n'

        # 重置合并字符串和大小计数器
        merged_text = text_value
        merged_text_size = new_text_size

    else:
        # 将新文本添加到合并字符串中，并更新大小计数器
        merged_text += (text_value + '\n')
        merged_text_size += new_text_size

with open('output.jsonl', 'w', encoding='utf-8') as f:
            f.write(json_string + '\n')
