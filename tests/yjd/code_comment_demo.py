from tree_sitter import Language, Parser  
import tree_sitter_python, tree_sitter_java, tree_sitter_go, tree_sitter_cpp, tree_sitter_javascript 

# PYTHON_LANGUAGE = Language(tree_sitter_python.language())  
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


def get_comment_text(node, comments=[]):
    if node.type == 'comment' or node.type == 'single_line_comment' or node.type == 'multi_line_comment' or node.type == 'line_comment':
        comments.append(node.text)
    for child in node.children:
        get_comment_text(child, comments)
    return comments

# 定义一个函数来递归遍历并打印树节点
def print_tree(node, indent=0):
    # 打印当前节点的类型和内容（如果有的话）
    print(' ' * indent + f'Node type: {node.type}, Text: {node.text.decode("utf8") if node.text else ""}')
    # 遍历当前节点的所有子节点
    for child in node.children:
        print_tree(child, indent + 2)

def extractNonCommentCode(nodes, codes):
    for node in nodes:
        if node.type == 'comment' or node.type == 'single_line_comment' or node.type == 'multi_line_comment' or node.type == 'line_comment':
        #    print(f'Node type: {node.type}, Text: {node.text.decode("utf8") if node.text else ""}')
           continue
        else:
           codes += node.text.decode("utf8") + '\n'
        if node.children:
            extractNonCommentCode(node.children, codes)
    return codes

def calculate_comment_ratio(code_text, comment_texts):
    total_code_chars = len(code_text)
    total_comment_chars = sum(len(comment) for comment in comment_texts)
    return total_comment_chars / total_code_chars if total_code_chars > 0 else 0

def main(file_path, language):
    with open(file_path, 'r', encoding='utf-8') as file:
        code_text = file.read()
 
    parser = Parser()
    parser.set_language(tree_sitter_x[language])
    tree = parser.parse(bytes(code_text, "utf8"))
 
    # # 从根节点开始打印树
    # print_tree(tree.root_node)


    # 提取非注释代码
    codes = ''
    print(extractNonCommentCode(tree.root_node.children, codes))

    # node = tree.root_node
    # print(f'Node type: {node.type}, Text: {node.text.decode("utf8") if node.text else ""}')
    # print('******************************')

    # node = tree.root_node.children
    # print(node)
   
 
if __name__ == "__main__":
    file_path = '/mnt/tmp/apps/cmss-yangjiandong/data-juicer/data_juicer/ops/filter/average_line_length_filter.py'
    main(file_path, 'python')
