import sys

from data_juicer.utils.constant import Fields, StatsKeys
from data_juicer.utils.model_utils import get_model, prepare_model

from ..base_op import AUTOINSTALL, OPERATORS, Filter

from ..op_fusion import INTER_LINES
from tree_sitter import Language, Parser  
import tree_sitter_python ,tree_sitter_java, tree_sitter_go, tree_sitter_cpp, tree_sitter_javascript 

OP_NAME = 'code_muti_language_syntax_filter'

@OPERATORS.register_module(OP_NAME)
@INTER_LINES.register_module(OP_NAME)
class CodeMutiLanguageSyntaxFilter(Filter):

    """Filter to keep samples with no code syntax error"""

    # 如果算子批量处理数据，输入不是一个样本而是一个batch，需要声明`_batched_op = True`
    _batched_op = True

    def __init__(self,
                 language = "python",
                 *args,
                 **kwargs):
        """
        Initialization method.

        :param args: extra args
        :param kwargs: extra args
        """
        super().__init__(*args, **kwargs)
        self.lauguage = language

        
    def compute_stats(self, samples):
        samples_list = samples[self.text_key]
        samples_stats = samples[Fields.stats]

        PYTHON_LANGUAGE = Language('/root/miniconda3/envs/data-juicer/lib/python3.8/site-packages/tree_sitter_python/_binding.abi3.so','python') 
        JAVA_LANGUAGE = Language('/root/miniconda3/envs/data-juicer/lib/python3.8/site-packages/tree_sitter_java/_binding.abi3.so','java')  
        GO_LANGUAGE = Language('/root/miniconda3/envs/data-juicer/lib/python3.8/site-packages/tree_sitter_go/_binding.abi3.so','go')  
        CPP_LANGUAGE = Language('/root/miniconda3/envs/data-juicer/lib/python3.8/site-packages/tree_sitter_cpp/_binding.abi3.so','cpp')  
        JAVASCRIPT_LANGUAGE = Language('/root/miniconda3/envs/data-juicer/lib/python3.8/site-packages/tree_sitter_javascript/_binding.abi3.so','javascript') 

        tree_sitter_x = {
        "python": PYTHON_LANGUAGE,
        "java": JAVA_LANGUAGE,
        "go": GO_LANGUAGE,
        "cpp": CPP_LANGUAGE,
        "javascript": JAVASCRIPT_LANGUAGE
        }

        parser = Parser()  
        parser.set_language(tree_sitter_x[self.lauguage])  
       
        for i, stat in enumerate(samples_stats):
            # check if it's computed already
            if StatsKeys.muti_code_syntax_error in stat:
                continue
            else:
                tree = parser.parse(bytes(samples_list[i], "utf8"))  
                samples_stats[i][StatsKeys.muti_code_syntax_error] = str(tree.root_node.has_error).upper()

        return samples

    def process(self, samples):
        if isinstance(samples[Fields.stats], list):
            return map(
                lambda stat: stat[StatsKeys.muti_code_syntax_error] == 'FALSE' , samples[Fields.stats])
        else:
            # single sample for ray filter
            samples[Fields.stats][StatsKeys.muti_code_syntax_error] == 'FALSE'
               
