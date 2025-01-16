#读取jsonl文件第一行

# -*- coding: utf-8 -*-
import json

with open('/mnt/tmp/apps/cmss-yangjiandong/data/opc/trace/filter-code_frac_string_filter.jsonl', 'r') as f:
    first_line = f.readline()

data = json.loads(first_line)
# data包含多行数据，打印第一行
print(data[0])
