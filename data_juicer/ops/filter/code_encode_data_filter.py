import sys

from data_juicer.utils.constant import Fields, StatsKeys
from data_juicer.utils.model_utils import get_model, prepare_model

from ..base_op import AUTOINSTALL, OPERATORS, Filter
from ..common import get_words_from_document
import regex as re
from collections import Counter

OP_NAME = 'code_encode_data_filter'

 # 计算代码文本中，包含的编码数据比例

@OPERATORS.register_module(OP_NAME)
class CodeEncodeDataFilter(Filter):
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
            if StatsKeys.encode_data_ratio in stat:
                continue
            else:
                patterns = {
                    'base64': re.compile(r'[a-zA-Z0-9+/\n=]{64,}'),
                    'hexadecimal': re.compile(r'(?:\b(?:0x|\\x)?[0-9a-fA-F]{2}(?:,|\b\s*)){8,}'),
                    'unicode': re.compile(r'(?:\\u[0-9a-fA-F]{4}){8,}')
                }

                total_matched_chars = 0
                for pattern in patterns.values():
                    matches = pattern.findall(samples_list[i])
                    for match in matches:
                        # if len(match) > 1024:
                        #      score = 1.0
                        total_matched_chars += len(match)

                encode_data_ratio = total_matched_chars / len(samples_list[i]) if len(samples_list[i]) > 0 else 0.0
                samples_stats[i][StatsKeys.encode_data_ratio] = encode_data_ratio
        return samples

    def process(self, samples):
        if isinstance(samples[Fields.stats], list):
            return map(
                lambda stat: stat[StatsKeys.encode_data_ratio] < self.ratio , samples[Fields.stats])
        else:
            # single sample for ray filter
            samples[Fields.stats][StatsKeys.encode_data_ratio] < self.ratio
