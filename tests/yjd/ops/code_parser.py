from tree_sitter import Language, Parser, Tree, Node
import tree_sitter_python, tree_sitter_java, tree_sitter_go, tree_sitter_cpp, tree_sitter_javascript 

from pygments import lex
from pygments.lexers import GoLexer, PythonLexer, CppLexer, JavascriptLexer,JavaLexer 

from typing import List, Dict, Any, Set, Optional, Generator
from loguru import logger
from conf import x_ast_info


tree_sitter_x = {
        "python": tree_sitter_python,
        "java": tree_sitter_java,
        "go": tree_sitter_go,
        "cpp": tree_sitter_cpp,
        "javascript": tree_sitter_javascript
    }


lexer_x = {
    "cpp": CppLexer(),
    "java": JavaLexer(),
    "python": PythonLexer(),
    "go": GoLexer(),
    "javascript": JavascriptLexer()
    }

class CodeParser():

    def __init__(self, language, *args, **kwargs):

        LANGUAGE = Language(tree_sitter_x[language].language())
        self.parser = Parser(LANGUAGE)
        self.ast_info = x_ast_info[language]
        self.lexer = lexer_x[language]

    # 遍历语法树
    @staticmethod
    def traverse_tree(tree: Tree) -> Generator[Node, None, None]:
        cursor = tree.walk()
        visited_children = False
        while True:
            if not visited_children:
                yield cursor.node
                if not cursor.goto_first_child():
                    visited_children = True
            elif cursor.goto_next_sibling():
                visited_children = False
            elif not cursor.goto_parent():
                break
    # 抽取类
    def get_class(self, content: str) -> List:
        """
        Return Class mete and content of the given code
        Return:   
            (name of the Class, content of the Class)
        """
        tree = self.parser.parse(bytes(content,"utf8"))
        paired = map(lambda node: 
                        (node.child_by_field_name('name').text.decode("utf-8") if node.child_by_field_name('name') else None,
                         node.text.decode("utf-8")),  
                        filter(lambda node: node.type in self.ast_info.class_def, self.traverse_tree(tree)))
        return list(paired)
    
    # 抽取函数
    def get_function(self, content: str) -> List:
        """
        Return function mete and content of the given code
        Return:   
            (name of the function, content of the function)
        """
        tree = self.parser.parse(bytes(content,"utf8"))
        paired = map(lambda node: 
                        (node.child_by_field_name('name').text.decode("utf-8") if node.child_by_field_name('name') else None,
                         node.text.decode("utf-8")),  
                        filter(lambda node: node.type in self.ast_info.function, self.traverse_tree(tree)))
        return list(paired)
    
    # 抽取代码块
    def get_block(self, content: str) -> List:
        """
        Return block mete and content of the given code
        Return:   
            (name of the block, content of the block)
        """
        tree = self.parser.parse(bytes(content,"utf8"))
        paired = map(lambda node: 
                        (node.type,
                         node.text.decode("utf-8")),  
                        filter(lambda node: node.type in self.ast_info.block, self.traverse_tree(tree)))
        return list(paired)

    # 抽取注释块 
    def get_comment(self, content: str) -> List:
        tree = self.parser.parse(bytes(content,"utf8"))
        paired = map(lambda node: 
                    (node.type, 
                    node.text.decode('utf-8')),  
                    filter(lambda node: node.type in self.ast_info.comment, self.traverse_tree(tree)))
        return list(paired)
    
    # 抽取括号块
    def get_parenthesized_nodes(self, content):
        tree = self.parser.parse(bytes(content,"utf8"))
        left = []
        right = []
        cursor = tree.walk()
        visited_children = False
        while True:
            if not visited_children:
                if cursor.node.type in ['(', '[', '{']:
                    left.append(cursor.node.parent)
                elif cursor.node.type in [')', ']', '}']:
                    right.append(cursor.node.parent)
                if not cursor.goto_first_child():
                    visited_children = True           
            elif cursor.goto_next_sibling():
                visited_children = False
            elif not cursor.goto_parent():
                break
        nodes = list(set(left) & set(right))
        nodes = map(lambda node: node.text.decode('utf-8'),  
                    filter(lambda node: node.start_point[0] == node.end_point[0] and node.child_count >= 3, nodes))
        return list(nodes)

    # 静态语法错误检查
    def check_error(self, content):
        tree = self.parser.parse(bytes(content,"utf8"))
        return tree.root_node.has_error
    def nodes_of_selected_type(self, content: str, node_type: List) -> List:
        """
        Return nodes of selected types
        Return:   
            (node, content of a node, name of a node)
        """
        tree = self.parser.parse(bytes(content,"utf8"))
        paired = map(lambda node: 
                        (node,
                         node.text.decode("utf-8"),
                         node.child_by_field_name('name').text.decode("utf-8") if node.child_by_field_name('name') else None),  
                        filter(lambda node: node.type in node_type, self.traverse_tree(tree)))
        return list(paired)
    def num_of_block(self, content) -> int:
        """
        Return type of children
        """
        node_type = self.ast_info.block + self.ast_info.function + self.ast_info.class_def + self.ast_info.type_def
        selected_type = self.nodes_of_selected_type(content, node_type)
        return len(selected_type)
    
    # 将源代码转换为tokens
    def line_tokenize(self, content: str) -> List:
        tokens = []
        # for line in  content.splitlines():
        tokens += list(map(lambda x: x[1], lex(content, self.lexer)))    
        # if tokens[-1] == '\n': # 这个分词器会多一个换行符
        #     tokens.pop()
        
        return tokens
        
    # 带前置docstring的function
    def func_with_docstring(self, content: str) -> List:
        tree = self.parser.parse(bytes(content,"utf8"))
        lines = content
        paired = map(lambda node: node.text.decode('utf-8'),  
                filter(lambda node: node.type in self.ast_info.function
                       and node.prev_sibling and node.prev_sibling.type in self.ast_info.doc_string
                       and len(node.prev_sibling.text.decode('utf-8')) > 30 
                       and (node.prev_sibling.prev_sibling and node.prev_sibling.prev_sibling.end_point[0] != node.prev_sibling.start_point[0]), self.traverse_tree(tree)))
        return list(paired)

class PythonCodeParser(CodeParser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # 抽取注释块 - python 1)#；2)'''、 """
    def get_comment(self, content: str) -> List:
        tree = self.parser.parse(bytes(content,"utf8"))
        paired = map(lambda node: 
                    (node.type if node.type in self.ast_info.comment else 'doc_string', 
                     node.text.decode('utf-8')),  
                    filter(lambda node: node.type in self.ast_info.comment 
                                        or (node.type == 'expression_statement' and node.child(0) and node.child(0).type == 'string'), 
                                        self.traverse_tree(tree)))
        return list(paired)
    
    # 带前置docstring的function
    def func_with_docstring(self, content: str) -> List:
        tree = self.parser.parse(bytes(content,"utf8"))
        paired = map(lambda node: node.text.decode('utf-8'),  
                    filter(lambda node: node.type in self.ast_info.function 
                           and node.prev_sibling and node.prev_sibling.type in self.ast_info.doc_string and node.prev_sibling.child(0) and node.prev_sibling.child(0).type  == 'string'
                           and len(node.prev_sibling.text.decode('utf-8')) > 30, self.traverse_tree(tree)))
        return list(paired)
    
    
class GoCodeParser(CodeParser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # 抽取go结构体
    def get_type(self, content: str) -> List:
        tree = self.parser.parse(bytes(content,"utf8"))
        paired = map(lambda node: 
                        (node.child(1).child_by_field_name('name').text.decode('utf-8'),
                         node.text.decode('utf-8')),  
                         filter(lambda node: node.type in self.ast_info.type, self.traverse_tree(tree)))    
        return list(paired)

class CPPCodeParser(CodeParser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # 抽取函数
    def get_function(self, content: str) -> List:
        """
        Return function mete and content of the given code
        Return:   
            (name of the function, content of the function)
        """
        tree = self.parser.parse(bytes(content,"utf8"))
        paired = map(lambda node: 
                        (node.child_by_field_name('declarator').text.decode("utf-8") if node.child_by_field_name('declarator') else None,
                         node.text.decode("utf-8")),  
                        filter(lambda node: node.type in self.ast_info.function, self.traverse_tree(tree)))
        return list(paired)
    
class JSCodeParser(CodeParser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
class JavaCodeParser(CodeParser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)