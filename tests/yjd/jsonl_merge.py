# 多个jsonl文件合并

import json
import glob

def merge_jsonl_files(input_path, output_path):

    with open(output_path, 'w') as outfile:
        for filename in glob.glob(input_path):
            with open(filename) as infile:
                for line in infile:
                    outfile.write(line)

merge_jsonl_files('/mnt/tmp/apps/cmss-yangjiandong/data-juicer/outputs/predict/the-stack-v2-full-Python/fliterscore/chunk_97_0.jsonl/*json',
                   '/mnt/tmp/apps/cmss-yangjiandong/data-juicer/outputs/predict/the-stack-v2-full-Python/fliterscore/merged.jsonl')