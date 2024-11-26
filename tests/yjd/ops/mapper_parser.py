from loguru import logger
from code_parser import * #PythonCodeParser, GoCodeParser, CPPCodeParser, JavaCodeParser, JSCodeParser

class Mapper():

    def __init__(self, *args, **kwargs):
        self.text_key = kwargs.get('text_key', 'text')
        
    def parser_init(self, sample):
        lang = sample["language"]
        if lang not in ["python","cpp", "java", "go", "javascript"]:
            logger.error(f"{lang} is not support")
            return None
        
        parser_route = {'javascript': JSCodeParser,
                        'python': PythonCodeParser,
                        'java': JavaCodeParser,
                        'go': GoCodeParser,
                        'cpp': CPPCodeParser
        }
        parser = parser_route[lang](lang)
        return parser
            
    def process(self, sample):
        raise NotImplementedError


class ErrorFilter(Mapper):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
    def process(self, sample):

        parser = self.parser_init(sample)
        if not parser:
            return sample
            
        res = parser.check_error(sample[self.text_key])
        sample["res"] = res
        return sample

class ComplexityFilter(Mapper):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
    def process(self, sample):

        parser = self.parser_init(sample)
        if not parser:
            return sample

        content = sample[self.text_key]
        res = 0
        if parser.check_error(content):
            res = 1
        else:
            if len(content.splitlines()) < 10 and parser.num_of_block(content) < 1:
                res =1
        sample["res"] = res
        return sample

class ExtractClass(Mapper):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
    def process(self, sample):

        parser = self.parser_init(sample)
        if not parser:
            return sample

        res = []
        if not parser.check_error(sample[self.text_key]):
            res =  parser.get_class(sample[self.text_key])
        sample["res"] = res
        return sample

class ExtractFunction(Mapper):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
    def process(self, sample):

        parser = self.parser_init(sample)
        if not parser:
            return sample

        res = []
        if not parser.check_error(sample[self.text_key]):
            res =  parser.get_function(sample[self.text_key])
        sample["res"] = res
        return sample

class ExtractBlock(Mapper):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
    def process(self, sample):

        parser = self.parser_init(sample)
        if not parser:
            return sample

        res = []
        if not parser.check_error(sample[self.text_key]):
            res =  parser.get_block(sample[self.text_key])
        sample["res"] = res
        return sample

        

class ExtractComment(Mapper):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
    def process(self, sample):

        parser = self.parser_init(sample)
        if not parser:
            return sample

        res = []
        if not parser.check_error(sample[self.text_key]):
            res =  parser.get_comment(sample[self.text_key])
        sample["res"] = res
        return sample

class ExtractLine(Mapper):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
    def process(self, sample):

        parser = self.parser_init(sample)
        if not parser:
            return sample

        res = []
        if not parser.check_error(sample[self.text_key]):
            res =  list(filter(lambda x : x.strip() !="", sample[self.text_key].splitlines()))
        sample["res"] = res
        return sample

       

class ExtractParenthes(Mapper):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
    def process(self, sample):

        parser = self.parser_init(sample)
        if not parser:
            return sample

        res = []
        if not parser.check_error(sample[self.text_key]):
            res =  parser.get_parenthesized_nodes(sample[self.text_key])
        sample["res"] = res
        return sample


class ExtractToken(Mapper):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
    def process(self, sample):

        parser = self.parser_init(sample)
        if not parser:
            return sample

        res = []
        if not parser.check_error(sample[self.text_key]):
            res =  parser.line_tokenize(sample[self.text_key])
        sample["res"] = res
        return sample

class FuncWithDocstring(Mapper):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
    def process(self, sample):

        parser = self.parser_init(sample)
        if not parser:
            return sample

        res = []
        if not parser.check_error(sample[self.text_key]):
            res =  parser.func_with_docstring(sample[self.text_key])
        sample["res"] = res
        return sample 

class AutoGeneratedFilter(Mapper):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
    def process(self, sample):

        res = False
        if 'auto' in sample[self.text_key][:500] and 'generated' in sample[self.text_key][:500]:
            res = True
        sample["res"] = res
        return sample