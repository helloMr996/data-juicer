# 根据代码质量分类器打分，过滤分数较低的代码
import sys

from data_juicer.utils.constant import Fields, StatsKeys
from data_juicer.utils.model_utils import get_model, prepare_model

from ..base_op import AUTOINSTALL, OPERATORS, Filter
from ..common import get_words_from_document


OP_NAME = 'score_filter'

@OPERATORS.register_module('score_filter')
class ScoreFilter(Filter):
    """Filter to doc_score < min_score"""

    # 如果算子批量处理数据，输入不是一个样本而是一个batch，需要声明`_batched_op = True`
    _batched_op = True

    def __init__(self,
                 min_score,
                 *args,
                 **kwargs):
        """
        Initialization method.

        :param args: extra args
        :param kwargs: extra args
        """
        super().__init__(*args, **kwargs)
        self.min_score = min_score
        

    def compute_stats(self, samples):
        # 通过质量分类器打分后，已经有了分数，此处不做处理
        return samples

    def process(self, samples):
        if isinstance(samples[Fields.score], list):
            return map(
                lambda score: score > self.min_score , samples[Fields.score])
        else:
            # single sample for ray filter
            samples[Fields.score] > self.min_score
               
