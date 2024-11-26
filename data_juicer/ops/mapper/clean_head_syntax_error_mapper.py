# Some code here has been modified from:
# https://github.com/togethercomputer/RedPajama-Data/tree/rp_v1/
# --------------------------------------------------------

import regex as re

from ..base_op import OPERATORS, Mapper


@OPERATORS.register_module('clean_head_syntax_error_mapper')
class CleanHeadSyntaxErrorMapper(Mapper):
    """Mapper to clean syntax error comments at the beginning of the text
    samples."""

    _batched_op = True

    def __init__(self, *args, **kwargs):
        """
        Initialization method.

        :param args: extra args
        :param kwargs: extra args
        """
        super().__init__(*args, **kwargs)

    def _process_single_sample(self, sample):

        lines = sample.split('\n')
        
        # 删除首行包含<gh_stars>、<reponame>、<filename>的记录
        if '<gh_stars>' in lines[0] or '<reponame>' in lines[0] or '<filename>' in lines[0]:
             sample = '\n'.join(lines[1:])
        return sample

    def process(self, samples):
        samples[self.text_key] = [
            self._process_single_sample(text)
            for text in samples[self.text_key]
        ]
        return samples
