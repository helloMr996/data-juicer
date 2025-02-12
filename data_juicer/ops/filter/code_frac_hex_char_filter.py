import sys

from data_juicer.utils.constant import Fields, StatsKeys
from data_juicer.utils.model_utils import get_model, prepare_model

from ..base_op import AUTOINSTALL, OPERATORS, Filter
from ..common import get_words_from_document
import regex as re
from collections import Counter

OP_NAME = 'code_frac_hex_char_filter'

 # 计算代码文本中，十六进制字词所占字符的比例

@OPERATORS.register_module(OP_NAME)
class CodeFracHexCharFilter(Filter):
    """Filter samples with encode data"""

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
            if StatsKeys.hex_data_ratio in stat:
                continue
            else:
                hex_count = sum(len(element) for element in re.findall(r'\b0[xX][0-9a-fA-F]+\b', samples_list[i]))

                hex_data_ratio = hex_count / len(samples_list[i]) if len(samples_list[i]) > 0 else 0.0
                samples_stats[i][StatsKeys.hex_data_ratio] = hex_data_ratio
        return samples

    def process(self, samples):
        if isinstance(samples[Fields.stats], list):
            return map(
                lambda stat: stat[StatsKeys.hex_data_ratio] < self.ratio , samples[Fields.stats])
        else:
            # single sample for ray filter
            samples[Fields.stats][StatsKeys.hex_data_ratio] < self.ratio
