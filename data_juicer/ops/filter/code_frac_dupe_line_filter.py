import sys

from data_juicer.utils.constant import Fields, StatsKeys
from data_juicer.utils.model_utils import get_model, prepare_model

from ..base_op import AUTOINSTALL, OPERATORS, Filter
from ..common import get_words_from_document
import regex as re
from collections import Counter

OP_NAME = 'code_frac_dupe_line_filter'

 # 计算代码文本中，代码行重复比例

@OPERATORS.register_module(OP_NAME)
class CodeFracDupeLineFilter(Filter):
    """Filter to keep samples with duplation ratio"""

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
    def _is_valid(self, line):
        invalid_lines = ['},']
        if line in invalid_lines or len(line) == 1:
            return False
        return True

    def compute_stats(self, samples):
        # 待处理代码文本
        samples_list = samples[self.text_key]
        # 统计字段
        samples_stats = samples[Fields.stats]

        for i, stat in enumerate(samples_stats):
            # check if it's computed already
            if StatsKeys.dupe_line_ratio in stat:
                continue
            else:
                lines = samples_list[i].split('\n')
                lines = [re.sub(r'\s+', '', line) for line in lines]
                line2count = Counter(lines)
                count = sum([v for k, v in line2count.items() if v != 1 and self._is_valid(k)])
                total = sum([v for v in line2count.values()])

                dupe_line_ratio = count/total if total>0 else 0
                samples_stats[i][StatsKeys.dupe_line_ratio] = dupe_line_ratio
        return samples

    def process(self, samples):
        if isinstance(samples[Fields.stats], list):
            return map(
                lambda stat: stat[StatsKeys.dupe_line_ratio] < self.ratio , samples[Fields.stats])
        else:
            # single sample for ray filter
            samples[Fields.stats][StatsKeys.dupe_line_ratio] < self.ratio
