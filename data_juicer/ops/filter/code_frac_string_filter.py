import sys

from data_juicer.utils.constant import Fields, StatsKeys
from data_juicer.utils.model_utils import get_model, prepare_model

from ..base_op import AUTOINSTALL, OPERATORS, Filter
from ..common import get_words_from_document
import regex as re

OP_NAME = 'code_frac_string_filter'

 # 计算代码文本中，字符串长度占总代码长度比例

@OPERATORS.register_module(OP_NAME)
class CodeFracStringFilter(Filter):
    """Filter to keep samples with string length"""

    # 如果算子批量处理数据，输入不是一个样本而是一个batch，需要声明`_batched_op = True`
    _batched_op = True

    def __init__(self,
                 ratio,
                 *args,
                 **kwargs):
        """
        Initialization method.
        :ratio 
        :param args: extra args
        :param kwargs: extra args
        """
        super().__init__(*args, **kwargs)
        self.ratio = ratio

    def compute_stats(self, samples):
        # 待处理代码文本
        samples_list = samples[self.text_key]
        # 统计字段
        samples_stats = samples[Fields.stats]

        for i, stat in enumerate(samples_stats):
            # check if it's computed already
            if StatsKeys.string_ratio in stat:
                continue
            else:
                # 提取优先级：三个单引号 > 三个双引号 > 单引号 > 双引号，使用非贪婪匹配
                string_pattern = re.compile(r'\'\'\'(.*?)\'\'\'|"""(.*?)"""|\'([^\n]*?)\'|"([^\n]*?)"', re.DOTALL)
                matches = string_pattern.findall(samples_list[i])
                string_list = []
                for match in matches:
                    for group in match:
                        if group:
                           string_list.append(group)
                string_length = sum([len(string) for string in string_list])
                total = len(samples_list[i])
                string_ratio = string_length/total if total>0 else 0
                samples_stats[i][StatsKeys.string_ratio] = string_ratio
        return samples

    def process(self, samples):
        if isinstance(samples[Fields.stats], list):
            return map(
                lambda stat: stat[StatsKeys.string_ratio] < self.ratio , samples[Fields.stats])
        else:
            # single sample for ray filter
            samples[Fields.stats][StatsKeys.string_ratio] < self.ratio
