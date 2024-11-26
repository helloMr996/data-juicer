import json  
  
def min_dc_score_jsonl_file_line_reader(file_path):  
    """  
    读取 JSONL 文件的某一行数据。  
  
    :param file_path: JSONL 文件的路径    
    :return: 读取到的 JSON 对象，如果行号超出范围则返回 None  
    """  
    try:
        min_dc_score = 1
        min_dc_score_text = None 
        with open(file_path, 'r', encoding='utf-8') as file:  
            for current_line_number, line in enumerate(file):  
                data = json.loads(line.strip())  
                min_dc_score_tmp = data['doc_score']
                if min_dc_score_tmp < min_dc_score:
                    min_dc_score = min_dc_score_tmp
                    min_dc_score_text = data['text']
        return min_dc_score_text  # 如果行号超出范围，返回 None  
    except FileNotFoundError:  
        print(f"文件 {file_path} 未找到")  
        return None  
    except json.JSONDecodeError:  
        print(f"文件 {file_path} 中存在无效的 JSON 数据")  
        return None  
def max_dc_score_jsonl_file_line_reader(file_path):  
    """  
    读取 JSONL 文件的某一行数据。  
  
    :param file_path: JSONL 文件的路径  
    :return: 读取到的 JSON 对象，如果行号超出范围则返回 None  
    """  
    try:
        max_dc_score = 0
        max_dc_score_text = None 
        with open(file_path, 'r', encoding='utf-8') as file:  
            for current_line_number, line in enumerate(file):  
                data = json.loads(line.strip())  
                max_dc_score_tmp = data['doc_score']
                if max_dc_score_tmp > max_dc_score:
                    max_dc_score = max_dc_score_tmp
                    max_dc_score_text = data['text']
        return max_dc_score_text  # 如果行号超出范围，返回 None  
    except FileNotFoundError:  
        print(f"文件 {file_path} 未找到")  
        return None  
    except json.JSONDecodeError:  
        print(f"文件 {file_path} 中存在无效的 JSON 数据")  
        return None 

# 获取得分小于某一个值的记录
def get_min_dc_score_records(file_path):
    min_dc_score_records = [] 
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                data = json.loads(line.strip())
                if data['doc_score'] < 0.01:
                    min_dc_score_records.append(data)

        return min_dc_score_records
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到")
        return None
    except json.JSONDecodeError:
        print(f"文件 {file_path} 中存在无效的 JSON 数据")
        return None

  
# 示例使用  
file_path = '/mnt/tmp/apps/cmss-yangjiandong/data-juicer/outputs/starcoderdata/python/fliterscore/train-00001-of-00059.jsonl/part-00000-2725f38a-1ac1-4b27-bedd-2f4605c408ec-c000.json'   
# data = min_dc_score_jsonl_file_line_reader(file_path)  
# print(data)  
min_dc_score_records = get_min_dc_score_records(file_path)
print(len(min_dc_score_records))
# 打印min_dc_score_records的每一条记录的长度
for record in min_dc_score_records:
    #计算行数，每行之间\n分割
     print(len(record))
    # print(len(record.split('\n')))
# print(min_dc_score_records[2]['text'])

