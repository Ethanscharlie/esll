from asttree import ASTNode

def generate_python(ast_nodes: list[ASTNode]) -> list[str]:
    my_code: list[str] = []

    my_code.append("""
def append(list, item):
    list.append(item)
def listget(list, index):
    return list[index]
    """)

    # PYTHON CODE GENERATION
    block = 0
    for node in ast_nodes:
        def get_block() -> str:
            return "    " * block

        def write_expression(node: ASTNode) -> str:
            def checkNode(testing_node: ASTNode | None):
                if testing_node == None:
                    raise SyntaxError("Node was null")

                expression = ""

                if testing_node.nodeType == ASTNode.NodeType.LITERAL:
                    expression += testing_node.value;
                    print(f"Literal value: {testing_node.value}")
                elif testing_node.nodeType == ASTNode.NodeType.IDENTIFIER:
                    expression += testing_node.name;

                elif node.nodeType == node.NodeType.FUNCTION_CALL:
                    if node.identifier == None:
                        raise SyntaxError("Null Identifier")

                    identifier = node.identifier.name
                    args = node.args
                    expression += f"{identifier}({', '.join([write_expression(arg) for arg in args])})"

                else:
                    print(testing_node.nodeType)
                    expression += write_expression(testing_node)

                return expression

            expression = ""
            if node.nodeType == ASTNode.NodeType.LITERAL:
                expression += node.value;
            elif node.nodeType == ASTNode.NodeType.IDENTIFIER:
                expression += node.name;

            elif node.nodeType == node.NodeType.FUNCTION_CALL:
                if node.identifier == None:
                    raise SyntaxError("Null Identifier")

                identifier = node.identifier.name
                args = node.args
                expression += f"{identifier}({', '.join([write_expression(arg) for arg in args])})"

            if node.nodeType == ASTNode.NodeType.ADD:
                expression += checkNode(node.first)
                expression += "+"
                expression += checkNode(node.second)
            
            elif node.nodeType == ASTNode.NodeType.SUBTRACT:
                expression += checkNode(node.first)
                expression += "-"
                expression += checkNode(node.second)
            
            elif node.nodeType == ASTNode.NodeType.MULTIPLY:
                expression += checkNode(node.first)
                expression += "*"
                expression += checkNode(node.second)
            
            elif node.nodeType == ASTNode.NodeType.DIVIDE:
                expression += checkNode(node.first)
                expression += "/"
                expression += checkNode(node.second)
            
            elif node.nodeType == ASTNode.NodeType.MODULUS:
                expression += checkNode(node.first)
                expression += "%"
                expression += checkNode(node.second)
            
            elif node.nodeType == ASTNode.NodeType.EQUALS:
                expression += checkNode(node.first)
                expression += "=="
                expression += checkNode(node.second)
            
            elif node.nodeType == ASTNode.NodeType.GREATER_THAN:
                expression += checkNode(node.first)
                expression += ">"
                expression += checkNode(node.second)
            
            elif node.nodeType == ASTNode.NodeType.LESS_THAN:
                expression += checkNode(node.first)
                expression += "<"
                expression += checkNode(node.second)
            
            elif node.nodeType == ASTNode.NodeType.AND:
                expression += checkNode(node.first)
                expression += " and "
                expression += checkNode(node.second)
            
            elif node.nodeType == ASTNode.NodeType.OR:
                expression += checkNode(node.first)
                expression += " or "
                expression += checkNode(node.second)
            
            return expression
            
        if node.nodeType == node.NodeType.VARIABLE_DECLARATION:
            if node.identifier == None:
                raise SyntaxError("Null Identifier")

            identifier = node.identifier.name

            if node.expression == None:
                raise SyntaxError("Null Expression")
            expression = node.expression

            my_code.append(f"{get_block()}{identifier} = {write_expression(expression)}")

        elif node.nodeType == node.NodeType.VARIABLE_ASSIGNMENT:
            if node.identifier == None:
                raise SyntaxError("Null Identifier")

            identifier = node.identifier.name

            if node.expression == None:
                raise SyntaxError("Null Expression")
            expression = node.expression

            my_code.append(f"{get_block()}{identifier} = {write_expression(expression)}")

        elif node.nodeType == node.NodeType.FUNCTION_DECLARATION:
            if node.identifier == None:
                raise SyntaxError("Null Identifier")

            identifier = node.identifier.name
            args = node.args
            my_code.append(f"{get_block()}def {identifier}({', '.join([arg.identifier.name for arg in args])}):")
            block += 1

        # elif node.nodeType == node.NodeType.FUNCTION_CALL:
        #     if node.identifier == None:
        #         raise SyntaxError("Null Identifier")
        #
        #     identifier = node.identifier.name
        #     args = node.args
        #     my_code.append(f"{get_block()}{identifier}({', '.join([write_expression(arg) for arg in args])})")

        elif node.nodeType == node.NodeType.IF:
            if node.expression == None:
                raise SyntaxError("Null Expression")

            expression = node.expression
            my_code.append(f"{get_block()}if {write_expression(expression)}:")
            block += 1

        elif node.nodeType == node.NodeType.RETURN:
            if node.expression == None:
                raise SyntaxError("Null Expression on return")

            expression = node.expression
            my_code.append(f"{get_block()}return {write_expression(expression)}")

        elif node.nodeType == node.NodeType.ELIF:
            if node.expression == None:
                raise SyntaxError("Null Expression")

            expression = node.expression
            block -= 1
            my_code.append(f"{get_block()}elif {write_expression(expression)}:")
            block += 1

        elif node.nodeType == node.NodeType.ELIF:
            block -= 1
            my_code.append(f"{get_block()}else:")
            block += 1

        elif node.nodeType == node.NodeType.WHILE:
            if node.expression == None:
                raise SyntaxError("Null Expression")

            expression = node.expression
            my_code.append(f"{get_block()}while {write_expression(expression)}:")
            block += 1

        elif node.nodeType == node.NodeType.END:
            if block == 0:
                raise SyntaxError("Misplaced End")
            block -= 1

    my_code.append("main()")
    return my_code

