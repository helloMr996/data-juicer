from tree_sitter import Language, Parser  
import tree_sitter_python ,tree_sitter_java, tree_sitter_go, tree_sitter_cpp, tree_sitter_javascript 

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
  
def has_syntax_error(code: str, language: str = "python") -> bool:  
    parser = Parser()  
    parser.set_language(tree_sitter_x[language])  
    tree = parser.parse(bytes(code, "utf8"))  
    # 检查解析是否成功 
    return tree.root_node.has_error

# 示例代码  
code = "# display\/dd_narrator.py \ndef read( script, flag ):\n\"\"\"\nFor a script dilineated into sections headed by flags starting with \"## \",\nfinds the section with the passed-in flag and returns it.\nIgnores lines starting with single #s. See \/script\/example .\n\"\"\"\n\tfor line in script:\n\t\tif line[0:2] == \"## \" and line[3:] == flag:\n\t\t\ttext = []\n\t\t\ttoRead = line + 1\n\t\t\twhile not script[toRead][0:2] == \"## \":\n\t\t\t\t#ignore comments\n\t\t\t\tif script[ toRead ][0] == \"#\":\n\t\t\t\t\ttoRead += 1\n\t\t\t\t#strip out blank lines at end of passages\n\t\t\t\t#(I like having those lines in cause it makes scripts pretty.)\n\t\t\t\telif script[ toRead ] == \"\" and script[ toRead + 1 ][0:2] == \"## \"\n\t\t\t\t\ttoRead += 1\n\t\t\t\t#add true lines to output\n\t\t\t\telse:\n\t\t\t\t\ttext.append( script[ toRead ] )\n\t\t\t\t\ttoRead += 1\n\t\t\treturn text\n\ndef genFlagList( dance ):\n\"\"\"\nAccepts a dance object and returns a list of flags.\nThis is akin to reading or parsing the condition of the dance game.\nThe flags can then be read using read().\n\"\"\"\n\tflagList = []\n\t\n\t#parse distance\n\tdistance = dance[\"game\"][\"d\"]\n\tif distance = 0:\n\t\tflagList.append( \"grapple\" )\n\telif abs(distance) = 1:\n\t\tflagList.append( \"shortRange\" )\n\telif abs(distance) = 2:\n\t\tflagList.append( \"midRange\" )\n\telif abs(distance) = 3:\n\t\tflagList.append( \"longRange\")\n\telif abs(distance) >= 4:\n\t\tflaglist.append( \"far\" )\n\ndef narrate( dance, script ):\n\"\"\"\nThis accepts a dance, gets all relevant flags, and returns their corresponding scripts.\nIn your games, you may wish to narrate flags in a certain order,\nso this may be too blunt for you.\n\"\"\"\n# in fact this might be too blunt for everyone...\n# how do I make it more versatile?\n\n\tnarrative = []\n\n\tflagList = genFlagList( dance )\n\tfor flag in flagList:\n\t\tnarrative += read( script, flag )\n\treturn narrative\n"

if has_syntax_error(code, 'python'):  
    print("Syntax error detected!")  
else:  
    print("No syntax error.")