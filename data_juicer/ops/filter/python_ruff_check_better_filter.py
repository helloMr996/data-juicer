import sys

from data_juicer.utils.constant import Fields, StatsKeys
from data_juicer.utils.model_utils import get_model, prepare_model

from ..base_op import AUTOINSTALL, OPERATORS, Filter
from ..common import get_words_from_document

import os
from collections import defaultdict
import json
import pandas as pd
import uuid
from multiprocessing import Pool, cpu_count
import subprocess

OP_NAME = 'python_ruff_check_better_filter'

@OPERATORS.register_module('python_ruff_check_better_filter')
class PythonRuffCheckBetterFilter(Filter):
    """Filter to keep samples with no code syntax error"""

    # 如果算子批量处理数据，输入不是一个样本而是一个batch，需要声明`_batched_op = True`
    _batched_op = True

    def __init__(self,
                 ruff_config_path,
                 ruff_rato,
                 tmp_dir=None,
                 *args,
                 **kwargs):
        """
        Initialization method.

        :param args: extra args
        :param kwargs: extra args
        """
        super().__init__(*args, **kwargs)
        self.ruff_config_path = ruff_config_path
        self.tmp_dir = tmp_dir
        self.ruff_rato = ruff_rato
        
    def get_file_name_without_extension(self, file_path):
        # 先获取文件名，然后分离扩展名
        base_name = os.path.basename(file_path)
        return os.path.splitext(base_name)[0]

    def run_ruff_check(self, python_file_path, config_path):
        # 定义Shell脚本的路径和参数
        script_path = '/mnt/tmp/apps/cmss-yangjiandong/data-juicer/data_juicer/ops/filter/ruff_check.sh'
        script_args = [python_file_path, config_path]  # 替换为你的实际参数

        # 构建完整的命令列表，包括脚本路径和参数
        complete_command = ['bash', script_path] + script_args

        # 使用subprocess.run执行脚本，并捕获输出和错误
        result = subprocess.run(complete_command, capture_output=True, text=True)

        grouped_counts = defaultdict(int)
  
        # 尝试将标准输出转换为JSON字典
        try:
            if not result.stdout:
                grouped_counts["F"] = 0
                grouped_counts["E"] = 0
            else:
                data = json.loads(result.stdout.strip())  # strip() 去除可能存在的首尾空白字符
                # 遍历数据，按照code首字母分组，并累加count
                for item in data:
                    if item['code'] is None:
                        # code_first_letter = item['name']
                        continue
                    else:
                        code_first_letter = item['code'][0]  # 获取code字段的首字母
                        grouped_counts[code_first_letter] += item['count']  # 累加count
        except json.JSONDecodeError as e:
            # 处理JSON解码错误
            print(f"Error decoding JSON: {e}")
            print(f'Return code: {result.returncode}')
            print(f'Standard Output:\n{result.stdout}')
            print("##################################")
            grouped_counts["F"] = 0
            grouped_counts["E"] = 0

        if 'F' not in  grouped_counts:
            grouped_counts["F"] = 0
        if 'E' not in grouped_counts:
            grouped_counts["E"] = 0

        return grouped_counts



    # 递归计算某一个目录及其子目录下python代码行数
    def count_non_empty_lines_in_file(self, filepath):
         """Count the number of non-empty lines in a file."""
         with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            return sum(1 for line in file if line.strip())  # line.strip() removes leading/trailing whitespace
        
    def compute_stats(self, samples):
        samples_list = samples[self.text_key]
        samples_stats = samples[Fields.stats]

        for i, stat in enumerate(samples_stats):
            # check if it's computed already
            if StatsKeys.ruff_EF_ratio in stat:
                continue
            else:
                # 生成一个随机的UUID字符串
                unique_string = str(uuid.uuid4())
                file_name = f'output_tmp_{unique_string}.py'
                # 构建代码文件的完整路径, 写文件
                file_path = os.path.join(self.tmp_dir, file_name)
               
                try:
                    with open(file_path, 'w') as f:
                        f.write(samples_list[i])
                    # 代码分析结果
                    grouped_counts = self.run_ruff_check(python_file_path=file_path, config_path=self.ruff_config_path)
                    # 代码总行数
                    total_line = self.count_non_empty_lines_in_file(filepath = file_path)
                    # 计算每个代码文件的TLOC
                    for letter, total_count in grouped_counts.copy().items():
                        grouped_counts[letter + "-TLOC"] = total_count * 10 / total_line

                    #增加统计字段
                    samples_stats[i][StatsKeys.ruff_EF_ratio] = grouped_counts['E-TLOC'] + grouped_counts['F-TLOC']

                except Exception as e:
                    print(f"Error processing file {file_path}: {str(e)}")
                    
                finally:
                    # 删除临时文件
                    os.remove(file_path)

        return samples
        

    def process(self, samples):
        if isinstance(samples[Fields.stats], list):
            return map(
                lambda stat: stat[StatsKeys.ruff_EF_ratio] < self.ruff_rato , samples[Fields.stats])
        else:
            # single sample for ray filter
            samples[Fields.stats][StatsKeys.ruff_EF_ratio] < self.ruff_rato
               
