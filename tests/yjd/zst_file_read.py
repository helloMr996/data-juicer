import zstandard as zstd
import ijson

def read_jsonl_zst_field(file_path, line_number, field_name):
    # 打开 zstd 压缩文件
    with open(file_path, 'rb') as f_in:
        decompressor = zstd.ZstdDecompressor()
        stream_reader = decompressor.stream_reader(f_in)
        
        # 使用 ijson 逐行读取 JSON Lines
        parser = ijson.parse(stream_reader)
        
        # 遍历 JSON 对象，直到找到指定的行
        current_line = 0
        for prefix, event, value in parser:
            if prefix == '' and event == 'map_key':
                # 忽略这一行，因为我们正在寻找开始的新对象
                continue
            elif prefix.endswith('}') and event == 'end_map':
                # 结束一个 JSON 对象，检查是否是我们需要的行
                current_line += 1
                if current_line == line_number:
                    # 回溯到上一个 'map_key' 事件（字段名）
                    last_key = None
                    for p, e, v in reversed(list(parser)):
                        if p == '' and e == 'map_key':
                            last_key = v
                            break
                    # 检查字段名并提取值
                    if last_key == field_name:
                        for p, e, v in parser:
                            if p.startswith(f'{last_key},') and e == 'string':
                                return v
                        return None  # 如果没有找到值（理论上不应该发生）
            elif current_line == line_number and prefix.startswith(f'{field_name},'):
                # 找到指定行的指定字段
                if event == 'string':  # 假设字段值是字符串类型
                    return value
    
    return None  # 如果未找到指定的行或字段

# 使用示例
file_path = '/mnt/tmp/apps/cmss-yangjiandong/data/the-stack-v2-go/chunk_0_0.jsonl.zst'
line_number = 2  # 注意：行号从1开始，但内部逻辑中从0开始计数并递增
field_name = 'test'

result = read_jsonl_zst_field(file_path, line_number, field_name)
print(f"The value of the field '{field_name}' on line {line_number} is: {result}")