# import pandas as pd

# # 读取 Parquet 文件
# parquet_file_path = '/mnt/tmp/apps/cmss-yangjiandong/ruff/high/data_100.parquet'
# df = pd.read_parquet(parquet_file_path)

# # 输出为 JSONL 文件
# jsonl_file_path = '/mnt/tmp/apps/cmss-yangjiandong/ruff/high/data_100.jsonl'
# with open(jsonl_file_path, 'w', encoding='utf-8') as f:
#     for index, row in df.iterrows():
#         json_record = row.to_json(orient='records', force_ascii=False)
#         # 去掉外面的数组符号 []，只保留内部的对象 {}
#         json_record = json_record[1:-1]  # 这里假设每行是一个对象，且数据框中每行都转化为一个对象

#         f.write(json_record + '\n')


# 注意：上面的代码中缺少了对 json 模块的导入，因为是在解释过程中逐步添加的。
# 在实际运行之前，请确保在脚本的顶部添加了以下导入语句：
import json
import pandas as pd

# Parquet 文件路径
parquet_file_path = '/mnt/tmp/apps/cmss-yangjiandong/ruff/high/data_100.parquet'

# 使用 pandas 读取 Parquet 文件
df = pd.read_parquet(parquet_file_path)

# 假设 Parquet 文件中有一个名为 'text' 的字段
# 检查 'text' 字段是否存在（可选步骤，但推荐）
if 'text' in df.columns:
    # 输出 JSONL 文件路径
    jsonl_file_path = '/mnt/tmp/apps/cmss-yangjiandong/ruff/high/data_100.jsonl'

    # 打开文件准备写入
    with open(jsonl_file_path, 'w', encoding='utf-8') as f:
        # 遍历 DataFrame 中的每一行
        for index, row in df.iterrows():
            # 提取 'text' 字段的值
            text_content = row['text']

            # 构建 JSON 对象
            json_object = {'text': text_content}

            # 将 JSON 对象转换为字符串，并写入文件
            # 每个 JSON 对象占一行（JSONL 格式）
            json_record = json.dumps(json_object, ensure_ascii=False)
            f.write(json_record + '\n')
else:
    print("Error: 'text' field not found in the Parquet file.")

