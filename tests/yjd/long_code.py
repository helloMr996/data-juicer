# import pyarrow as pa
# import pyarrow.parquet as pq

# # Parquet文件路径
# parquet_file = 'your_file.parquet'

# # 读取Parquet文件中的'text'列到一个Arrow Array
# text_column = pq.read_table(parquet_file).column('text')

# max_bytes = 256*1024
# size_in_bytes = 0
# tmp = None
# # 遍历Arrow Array的每个元素（即'text'列的每个值）
# for text_value in text_column:
#     # print(text_value.as_py())  # 对于字符串列，使用.as_py()方法将其转换为Python字符串
#     size_in_bytes += len(text_value.encode('utf-8'))
#     tmp = text_value + ''
#     if size_in_bytes > max_bytes:
#         print(f'过大的文本：{text_value}')


# import pandas as pd
# import pyarrow as pa
# import pyarrow.parquet as pq
# import io

# # Parquet文件路径
# input_parquet_file = '/mnt/tmp/apps/cmss-yangjiandong/staging_stack_v1/python/data-00000-of-00144.parquet'

# # 读取Parquet文件到DataFrame
# df = pd.read_parquet(input_parquet_file)

# # 初始化合并字符串和字节大小计数器
# merged_text = ""
# merged_text_size = 0

# # 定义输出Parquet文件的索引
# output_file_index = 1

# # 遍历DataFrame的每一行
# for index, row in df.iterrows():
#     # 获取text列的值，并将其转换为字符串（以防万一它是其他类型）
#     text_value = str(row['content'])
    
#     # 计算添加新文本后的总大小（以字节为单位）
#     new_text_size = len(text_value.encode('utf-8'))
    
#     # 检查是否超过256KB限制
#     if merged_text_size + new_text_size > 262144:  # 256KB = 262144字节
#         # 创建一个新的DataFrame来存储当前合并的文本，并写入Parquet文件
#         temp_df = pd.DataFrame({'content': [merged_text]})
#         table = pa.Table.from_pandas(temp_df)
#         output_parquet_file = f'output_{output_file_index}.parquet'
#         pq.write_table(table, output_parquet_file)
        
#         # 重置合并字符串和大小计数器
#         merged_text = text_value
#         merged_text_size = new_text_size
#         output_file_index += 1
#     else:
#         # 将新文本添加到合并字符串中，并更新大小计数器
#         merged_text += (text_value + '</eos_token>')
#         merged_text_size += new_text_size

# # 处理完所有行后，检查是否有剩余文本需要写入
# if merged_text:
#     # 创建一个新的DataFrame来存储剩余合并的文本，并写入Parquet文件
#     temp_df = pd.DataFrame({'content': [merged_text]})
#     table = pa.Table.from_pandas(temp_df)
#     output_parquet_file = f'output_{output_file_index}.parquet'
#     pq.write_table(table, output_parquet_file)




import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import io
import json

# Parquet文件路径
input_parquet_file = '/mnt/tmp/apps/cmss-yangjiandong/staging_stack_v1/python/data-00000-of-00144.parquet'

# 读取Parquet文件到DataFrame
df = pd.read_parquet(input_parquet_file)

# 初始化合并字符串和字节大小计数器
merged_text = ""
merged_text_size = 0

# 定义输出Parquet文件的索引
output_file_index = 1


# 将字符串填写到JSON模板中
json_string = ''

# 遍历DataFrame的每一行
for index, row in df.iterrows():
    # 获取text列的值，并将其转换为字符串（以防万一它是其他类型）
    text_value = str(row['content'])
    
    # 计算添加新文本后的总大小（以字节为单位）
    new_text_size = len(text_value.encode('utf-8'))
    
    # 检查是否超过256KB限制
    if merged_text_size + new_text_size > 262144:  # 256KB = 262144字节

        filled_json = {
            "text": merged_text
        }
        json_string += json.dumps(filled_json) + '\n'

        # 重置合并字符串和大小计数器
        merged_text = text_value
        merged_text_size = new_text_size
        output_file_index += 1
    else:
        # 将新文本添加到合并字符串中，并更新大小计数器
        merged_text += (text_value + '</eos_token>')
        merged_text_size += new_text_size

with open('output.jsonl', 'w', encoding='utf-8') as f:
            f.write(json_string + '\n')
