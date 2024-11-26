import json  
  
def read_jsonl_line(file_path, line_number):  
    """  
    读取 JSONL 文件的某一行数据。  
  
    :param file_path: JSONL 文件的路径  
    :param line_number: 要读取的行号（从 0 开始）  
    :return: 读取到的 JSON 对象，如果行号超出范围则返回 None  
    """  
    try:  
        with open(file_path, 'r', encoding='utf-8') as file:  
            for current_line_number, line in enumerate(file):  
                if current_line_number == line_number:  
                    return json.loads(line.strip())  
        return None  # 如果行号超出范围，返回 None  
    except FileNotFoundError:  
        print(f"文件 {file_path} 未找到")  
        return None  
    except json.JSONDecodeError:  
        print(f"文件 {file_path} 中存在无效的 JSON 数据")  
        return None  
  
# 示例使用  
file_path = '/mnt/tmp/apps/cmss-yangjiandong/staging_stack_v1/filter/staging-stack-v1-python-filter.parquet'  
line_number = 5  # 读取第三行（行号从 0 开始）  
data = read_jsonl_line(file_path, line_number)  
if data:  
    print(data)  
else:  
    print("未找到指定行或文件读取失败")



def count_jsonl_lines(file_path):  
    """  
    计算 JSONL 文件的总行数。  
  
    :param file_path: JSONL 文件的路径  
    :return: 文件的总行数  
    """  
    try:  
        with open(file_path, 'r', encoding='utf-8') as file:  
            return sum(1 for _ in file)  
    except FileNotFoundError:  
        print(f"文件 {file_path} 未找到")  
        return -1  # 或者你可以选择返回其他表示错误的值  
  
# 示例使用  
file_path = '/mnt/tmp/apps/cmss-yangjiandong/staging_stack_v1/filter/staging-stack-v1-python-filter.parquet'  
total_lines = count_jsonl_lines(file_path)  
if total_lines != -1:  
    print(f"JSONL 文件 {file_path} 的总行数是: {total_lines}")  
else:  
    print("无法计算文件的总行数")