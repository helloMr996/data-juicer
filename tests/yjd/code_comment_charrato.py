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
 
    root_node = tree.root_node
    comments = get_comment_text(root_node)
    # print('*************************************************************')
    # print(comments)
 
    comment_ratio = calculate_comment_ratio(code_text, comments)
 
    print(f"Total comments characters: {sum(len(comment) for comment in comments)}")
    print(f"Total code characters: {len(code_text)}")
    print(f"Comment ratio: {comment_ratio:.2%}")
 
if __name__ == "__main__":
    file_path = '/mnt/tmp/apps/cmss-yangjiandong/data-juicer/tests/yjd/WeiXinConstants.java'
    main(file_path, 'java')
