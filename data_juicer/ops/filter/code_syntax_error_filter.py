import sys

from data_juicer.utils.constant import Fields, StatsKeys
from data_juicer.utils.model_utils import get_model, prepare_model

from ..base_op import AUTOINSTALL, OPERATORS, Filter
from ..common import get_words_from_document

from tree_sitter import Language, Parser  
import tree_sitter_python

OP_NAME = 'code_syntax_error_filter'

@OPERATORS.register_module('code_syntax_error_filter')
class CodeSyntaxErrorFilter(Filter):
    """Filter to keep samples with no code syntax error"""

    # 如果算子批量处理数据，输入不是一个样本而是一个batch，需要声明`_batched_op = True`
    _batched_op = True

    def __init__(self,
                 *args,
                 **kwargs):
        """
        Initialization method.

        :param args: extra args
        :param kwargs: extra args
        """
        super().__init__(*args, **kwargs)
        

    def compute_stats(self, samples):
        samples_list = samples[self.text_key]
        samples_stats = samples[Fields.stats]
        
        PYTHON_LANGUAGE = Language('/root/miniconda3/envs/data-juicer/lib/python3.8/site-packages/tree_sitter_python/_binding.abi3.so','python') 
        parser = Parser()  
        parser.set_language(PYTHON_LANGUAGE)  
        self.parser = parser

        for i, stat in enumerate(samples_stats):
            # check if it's computed already
            if StatsKeys.code_syntax_error in stat:
                continue
            else:
                # print("#########################")
                # print(samples_list[i])
                tree = self.parser.parse(bytes(samples_list[i], "utf8"))  
                samples_stats[i][StatsKeys.code_syntax_error] = str(tree.root_node.has_error).upper()

        return samples

    def process(self, samples):
        if isinstance(samples[Fields.stats], list):
            return map(
                lambda stat: stat[StatsKeys.code_syntax_error] == 'FALSE' , samples[Fields.stats])
        else:
            # single sample for ray filter
            samples[Fields.stats][StatsKeys.code_syntax_error] == 'FALSE'
               
