from dataclasses import dataclass, field

@dataclass
class AstInfo:
    class_def: list = field(default_factory=list)
    function: list = field(default_factory=list)
    block: list = field(default_factory=list)
    comment: list = field(default_factory=list)
    type_def: list = field(default_factory=list)
    interface: list = field(default_factory=list)
    doc_string: list = field(default_factory=list)


python_ast_info = AstInfo(class_def =  ["class_definition"],
                          function = ["function_definition"],
                          block = ["try_statement", "with_statement", "if_statement", "for_statement", "while_statement", "match_statement"],
                          comment = ["comment"],
                          doc_string = ["expression_statement"]
                    )

go_ast_info = AstInfo(type_def =  ["type_declaration"],
                          function = ["function_declaration", "method_declaration"],
                          block = ["defer_statement", "labeled_statement", "select_statement", "go_statement", "try_statement", "with_statement", "if_statement", "for_statement", "while_statement", "expression_switch_statement"],
                          comment = ["comment"],
                          doc_string = ["comment"]
                    )

cpp_ast_info = AstInfo(class_def =  ["class_specifier"], # "namespace_definition"
                          function = ["function_definition"],
                          block = ["labeled_statement", "try_statement", "if_statement", "for_statement", "while_statement", "do_statement", "switch_statement"],
                          comment = ["comment"],
                          doc_string = ["comment"]
                          
                    )

java_ast_info = AstInfo(class_def =  ["class_declaration"],
                          function = ["method_declaration"], # constructor_declaration,
                          block = ["try_statement", "try_with_resources_statement", "if_statement", "switch_expression", "for_statement", "enhanced_for_statement", "while_statement", "labeled_statement", "synchronized_statement"],
                          comment = ["line_comment","block_comment"],
                          type_def = ["annotation_type_declaration", "enum_declaration"],
                          interface = ["interface_declaration"],
                          doc_string = ["block_comment"]
                    )

js_ast_info = AstInfo(class_def =  ["class_declaration"],
                          function =["function_declaration"],
                          block = ["if_statement", "switch_statement", "for_statement", "for_in_statement", "while_statement", "do_statement", "switch_statement"],
                          comment = ["comment"],
                          doc_string = ["comment"]
                    )

x_ast_info = {
        "python": python_ast_info,
        "java": java_ast_info,
        "go": go_ast_info,
        "cpp": cpp_ast_info,
        "javascript": js_ast_info
    }