import sys

from data_juicer.utils.constant import Fields, StatsKeys
from data_juicer.utils.model_utils import get_model, prepare_model

from ..base_op import AUTOINSTALL, OPERATORS, Filter
from ..common import get_words_from_document

from tree_sitter import Language, Parser  
import tree_sitter_python ,tree_sitter_java, tree_sitter_go, tree_sitter_cpp, tree_sitter_javascript

OP_NAME = 'code_comment_rato_filter'

@OPERATORS.register_module('code_comment_rato_filter')
class CodeCommentRatoFilter(Filter):
    """Filter to keep samples with no code syntax error"""

    # 如果算子批量处理数据，输入不是一个样本而是一个batch，需要声明`_batched_op = True`
    _batched_op = True

    def __init__(self,
                 method,
                 ratio,
                 language,
                 *args,
                 **kwargs):
        """
        Initialization method.

        :param args: extra args
        :param kwargs: extra args
        """
        super().__init__(*args, **kwargs)
        self.method = method
        self.ratio = ratio
        self.language = language

    # 获取代码注释内容
    def get_comment_text(self, node, comments=[]):
        if node.type == 'comment' or node.type == 'single_line_comment' or node.type == 'multi_line_comment' or node.type == 'line_comment':
            comments.append(node.text.decode('utf8'))
        for child in node.children:
             self.get_comment_text(child, comments)
        return comments
    
    # 计算总行数
    def count_total_lines(self, sample):
        lines = sample.split('\n')
        non_empty_line_count = 0
        for line in lines:
            if line.strip():
                non_empty_line_count += 1
        return non_empty_line_count

    def compute_stats(self, samples):

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
        parser.set_language(tree_sitter_x[self.language])  

        samples_list = samples[self.text_key]
        samples_stats = samples[Fields.stats]
        
        for i, stat in enumerate(samples_stats):
            # check if it's computed already
            if StatsKeys.comment_ratio in stat:
                continue
            else:
                total_lines = self.count_total_lines(samples_list[i])
                tree = parser.parse(bytes(samples_list[i], "utf8"))  
                root_node = tree.root_node
                comments = self.get_comment_text(root_node)
                # 计算注释行占比
                if self.method == 'line-rato':
                    comment_ratio = len(comments) / total_lines
                    # print('##########################################')
                    # print(comment_ratio)
                
                # 计算注释字符占比
                else:
                    total_code_chars = len(samples_list[i])
                    total_comment_chars = sum(len(comment) for comment in comments)
                    comment_ratio = total_comment_chars / total_code_chars if total_code_chars > 0 else 0
                    # print('##########################################')
                    # print(comment_ratio)

                samples_stats[i][StatsKeys.comment_ratio] = comment_ratio

        return samples

    def process(self, samples):
        if isinstance(samples[Fields.stats], list):
            return map(
                lambda stat: stat[StatsKeys.comment_ratio] < self.ratio , samples[Fields.stats])
        else:
            # single sample for ray filter
            samples[Fields.stats][StatsKeys.comment_ratio] < self.ratio
               
