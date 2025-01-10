from __future__ import annotations
from ast import AST, Expression, arguments, expr, operator
from dataclasses import dataclass, field
import copy
from enum import Enum
from os import confstr, walk

variable_tracker: dict[str, str] = {}

class EsllType(Enum):
    VOID = 0
    INTEGER = 1
    DECIMAL = 2
    BOOLEAN = 3
    STRING = 4


@dataclass 
class ASTNode:
    class NodeType(Enum):
        NONE = 22
        IDENTIFIER = 0
        LITERAL = 1
        TYPE = 2
    
        ADD = 3
        SUBTRACT = 4
        MULTIPLY = 5
        DIVIDE = 6
        MODULUS = 7

        EQUALS = 17
        GREATER_THAN = 18
        LESS_THAN = 19
        AND = 20
        OR = 21
    
        VARIABLE_DECLARATION = 8
        FUNCTION_DECLARATION = 9
        VARIABLE_ASSIGNMENT = 10
        FUNCTION_CALL = 11
    
        FUNCTION_ARGUMENT_DECLARATION = 16
    
        IF = 12
        WHILE = 13
        END = 14
        ELIF = 23
        ELSE = 24
        RETURN = 25

    nodeType: NodeType

    value: str = ""
    name: str = ""
    first: ASTNode | None = None
    second: ASTNode | None = None
    esllType: EsllType = EsllType.VOID
    identifier: ASTNode | None = None
    expression: ASTNode | None = None
    args: list = field(default_factory=list)

@dataclass 
class Token:
    class TOKEN_TYPE(Enum):
        IDENTIFIER = 0
        LITERAL = 1
        TYPE = 2
    
        ADD = 3
        SUBTRACT = 4
        MULTIPLY = 5
        DIVIDE = 6
        MODULUS = 7

        EQUALS = 17
        GREATER_THAN = 18
        LESS_THAN = 19
        AND = 20
        OR = 21
    
        IF = 12
        WHILE = 13
        END = 14
        ELIF = 23
        ELSE = 24
        RETURN = 25

        OPENING_PARENTHESIS = 15
        CLOSING_PARENTHESIS = 16
        SEPERATOR = 22

    token_type: TOKEN_TYPE
    value: str

def main() -> None:
    ESLL_FILE = "main.esll"

    my_code: list[str] = []

    full_text = ""
    with open(ESLL_FILE, "r") as f:
        full_text = f.read()

    lines = full_text.split("\n")
    tokenized_lines: list[list[Token]] = []
    in_quotes = False
    word_collecter = ""

    for line in lines:
        tokenized_lines.append([])

        def add_word_token(word: str):
            token_type = Token.TOKEN_TYPE.IDENTIFIER

            if word.replace(".", "").isnumeric():
                token_type = Token.TOKEN_TYPE.LITERAL

            if word == "false" or word == "true":
                token_type = Token.TOKEN_TYPE.LITERAL

            elif word == "String":
                token_type = Token.TOKEN_TYPE.TYPE

            elif word == "Integer":
                token_type = Token.TOKEN_TYPE.TYPE

            elif word == "Decimal":
                token_type = Token.TOKEN_TYPE.TYPE

            elif word == "Boolean":
                token_type = Token.TOKEN_TYPE.TYPE

            elif word == "Void":
                token_type = Token.TOKEN_TYPE.TYPE

            elif word == "if":
                token_type = Token.TOKEN_TYPE.IF

            elif word == "while":
                token_type = Token.TOKEN_TYPE.WHILE

            elif word == "end":
                token_type = Token.TOKEN_TYPE.END

            elif word == "elif":
                token_type = Token.TOKEN_TYPE.ELIF

            elif word == "else":
                token_type = Token.TOKEN_TYPE.ELSE

            elif word == "return":
                token_type = Token.TOKEN_TYPE.RETURN

            tokenized_lines[-1].append(Token(token_type, word))

        for i in range(len(line)):
            c = line[i]

            added_to_word = False
            token = Token(Token.TOKEN_TYPE.IDENTIFIER, "")

            if in_quotes:
                tokenized_lines[-1][-1].value += c

                if c == "\"":
                    in_quotes = False
                    continue

            elif c == " ":
                pass

            elif c == ",":
                token = Token(Token.TOKEN_TYPE.SEPERATOR, c)

            elif c == "+":
                token = Token(Token.TOKEN_TYPE.ADD, c)

            elif c == "-":
                token = Token(Token.TOKEN_TYPE.SUBTRACT, c)

            elif c == "*":
                token = Token(Token.TOKEN_TYPE.MULTIPLY, c)

            elif c == "/":
                token = Token(Token.TOKEN_TYPE.DIVIDE, c)

            elif c == "%":
                token = Token(Token.TOKEN_TYPE.MODULUS, c)

            elif c == "&":
                token = Token(Token.TOKEN_TYPE.AND, c)

            elif c == "|":
                token = Token(Token.TOKEN_TYPE.OR, c)

            elif c == ">":
                token = Token(Token.TOKEN_TYPE.GREATER_THAN, c)

            elif c == "<":
                token = Token(Token.TOKEN_TYPE.LESS_THAN, c)

            elif c == "=":
                token = Token(Token.TOKEN_TYPE.EQUALS, c)

            elif c == "(":
                token = Token(Token.TOKEN_TYPE.OPENING_PARENTHESIS, c)

            elif c == ")":
                token = Token(Token.TOKEN_TYPE.CLOSING_PARENTHESIS, c)

            elif c == "\"":
                in_quotes = True
                token = Token(Token.TOKEN_TYPE.LITERAL, "\"")

            else: 
                added_to_word = True
                word_collecter += c

            if not added_to_word and len(word_collecter) > 0:
                add_word_token(word_collecter)
                word_collecter = ""

            if not (token.token_type == Token.TOKEN_TYPE.IDENTIFIER and token.value == ""):
                tokenized_lines[-1].append(token)
        
        if len(word_collecter) > 0:
            add_word_token(word_collecter)
            word_collecter = ""

    print(" -- TOKENS -- ")
    for tokenized_line in tokenized_lines:
        print("LINE")
        for token in tokenized_line:
            print(token)

    my_code.append("""
def append(list, item):
    list.append(item)
def listget(list, index):
    return list[index]
    """)

    ast_nodes: list[ASTNode] = []

    # CREATE ESL TREE
    print(" -- ESL TREE -- ")
    for i, tokenized_line in enumerate(tokenized_lines):
        def get_type(name: str) -> EsllType:
            if name == "String": return EsllType.STRING
            elif name == "Integer": return EsllType.INTEGER
            elif name == "Decimal": return EsllType.DECIMAL
            elif name == "Void": return EsllType.VOID
            elif name == "Boolean": return EsllType.BOOLEAN
            return EsllType.VOID

        def make_expression_node(tokens: list[Token]) -> ASTNode:
            def make_data_node(data_token: Token) -> ASTNode:
                data_node = ASTNode(ASTNode.NodeType.NONE)

                if data_token.token_type == Token.TOKEN_TYPE.IDENTIFIER:
                    data_node = ASTNode(ASTNode.NodeType.IDENTIFIER)
                    data_node.name = data_token.value

                elif data_token.token_type == Token.TOKEN_TYPE.LITERAL:
                    data_node = ASTNode(ASTNode.NodeType.LITERAL)
                    data_node.value = data_token.value

                return data_node

            node = make_data_node(tokens[0])

            i = 0
            while i < len(tokens):
                token = tokens[i]

                if token.token_type == Token.TOKEN_TYPE.ADD:
                    new_node = ASTNode(ASTNode.NodeType.ADD)
                    new_node.first = node
                    new_node.second = make_data_node(tokens[i + 1])
                    i += 1
                    node = new_node

                elif token.token_type == Token.TOKEN_TYPE.SUBTRACT:
                    new_node = ASTNode(ASTNode.NodeType.SUBTRACT)
                    new_node.first = node
                    new_node.second = make_data_node(tokens[i + 1])
                    i += 1
                    node = new_node

                elif token.token_type == Token.TOKEN_TYPE.MULTIPLY:
                    new_node = ASTNode(ASTNode.NodeType.MULTIPLY)
                    new_node.first = node
                    new_node.second = make_data_node(tokens[i + 1])
                    i += 1
                    node = new_node

                elif token.token_type == Token.TOKEN_TYPE.DIVIDE:
                    new_node = ASTNode(ASTNode.NodeType.DIVIDE)
                    new_node.first = node
                    new_node.second = make_data_node(tokens[i + 1])
                    i += 1
                    node = new_node

                elif token.token_type == Token.TOKEN_TYPE.MODULUS:
                    new_node = ASTNode(ASTNode.NodeType.MODULUS)
                    new_node.first = node
                    new_node.second = make_data_node(tokens[i + 1])
                    i += 1
                    node = new_node

                elif token.token_type == Token.TOKEN_TYPE.GREATER_THAN:
                    new_node = ASTNode(ASTNode.NodeType.GREATER_THAN)
                    new_node.first = node
                    new_node.second = make_data_node(tokens[i + 1])
                    i += 1
                    node = new_node

                elif token.token_type == Token.TOKEN_TYPE.LESS_THAN:
                    new_node = ASTNode(ASTNode.NodeType.LESS_THAN)
                    new_node.first = node
                    new_node.second = make_data_node(tokens[i + 1])
                    i += 1
                    node = new_node
                    
                elif token.token_type == Token.TOKEN_TYPE.EQUALS:
                    new_node = ASTNode(ASTNode.NodeType.EQUALS)
                    new_node.first = node
                    new_node.second = make_data_node(tokens[i + 1])
                    i += 1
                    node = new_node
                    
                elif token.token_type == Token.TOKEN_TYPE.OR:
                    new_node = ASTNode(ASTNode.NodeType.OR)
                    new_node.first = node
                    new_node.second = make_data_node(tokens[i + 1])
                    i += 1
                    node = new_node

                elif token.token_type == Token.TOKEN_TYPE.AND:
                    new_node = ASTNode(ASTNode.NodeType.AND)
                    new_node.first = node
                    new_node.second = make_data_node(tokens[i + 1])
                    i += 1
                    node = new_node

                print(f"{node} from token: {token}")
                i += 1

            return node

        node: ASTNode

        if len(tokenized_line) == 0:
            continue

        if tokenized_line[0].token_type == Token.TOKEN_TYPE.TYPE:
            declarationType = tokenized_line[0].value

            if tokenized_line[1].token_type == Token.TOKEN_TYPE.IDENTIFIER:
                identifier = tokenized_line[1].value
                identifierNode = ASTNode(ASTNode.NodeType.IDENTIFIER)
                identifierNode.name = identifier

                if tokenized_line[2].token_type == Token.TOKEN_TYPE.OPENING_PARENTHESIS:
                    node = ASTNode(ASTNode.NodeType.FUNCTION_DECLARATION)
                    node.esllType = get_type(declarationType)
                    node.identifier = identifierNode

                    arg_collector: list[Token] = []

                    def make_argdec_node(arg_collector: list[Token]) -> ASTNode:
                        if len(arg_collector) != 2:
                            raise SyntaxError("Argument definition as extra token")

                        if arg_collector[0].token_type != Token.TOKEN_TYPE.TYPE:
                            raise SyntaxError("Type expected on argument definition")

                        if arg_collector[1].token_type != Token.TOKEN_TYPE.IDENTIFIER:
                            raise SyntaxError("identifier expected on argument definition")

                        new_arg_node = ASTNode(ASTNode.NodeType.FUNCTION_ARGUMENT_DECLARATION)

                        new_arg_node.esllType = get_type(arg_collector[0].value)

                        new_arg_node.identifier = ASTNode(ASTNode.NodeType.IDENTIFIER)
                        new_arg_node.identifier.name = arg_collector[1].value

                        return new_arg_node

                    for arg_token in tokenized_line[3:-1]: 
                        if arg_token.token_type == Token.TOKEN_TYPE.SEPERATOR:
                            node.args.append(make_argdec_node(arg_collector))
                            arg_collector = []
                        else:
                            arg_collector.append(arg_token)

                    if len(arg_collector) > 0: node.args.append(make_argdec_node(arg_collector))
                    ast_nodes.append(node)
                else:
                    node = ASTNode(ASTNode.NodeType.VARIABLE_DECLARATION)
                    node.esllType = get_type(declarationType)
                    node.identifier = identifierNode
                    node.expression = make_expression_node(tokenized_line[2:])
                    ast_nodes.append(node)
            else:
                raise SyntaxError("Identifier expected")

        elif tokenized_line[0].token_type == Token.TOKEN_TYPE.IDENTIFIER:
            identifier = tokenized_line[0].value
            identifierNode = ASTNode(ASTNode.NodeType.IDENTIFIER)
            identifierNode.name = identifier

            if tokenized_line[1].token_type == Token.TOKEN_TYPE.OPENING_PARENTHESIS:
                node = ASTNode(ASTNode.NodeType.FUNCTION_CALL)
                node.identifier = identifierNode

                if tokenized_line[-1].token_type != Token.TOKEN_TYPE.CLOSING_PARENTHESIS:
                    raise SyntaxError("Missing ) on function call")

                expression_collector: list[Token] = []
                for arg_token in tokenized_line[2:-1]: 
                    if arg_token.token_type == Token.TOKEN_TYPE.SEPERATOR:
                        node.args.append(make_expression_node(expression_collector))
                        expression_collector = []
                    else:
                        expression_collector.append(arg_token)

                node.args.append(make_expression_node(expression_collector))
                ast_nodes.append(node)

            else:
                node = ASTNode(ASTNode.NodeType.VARIABLE_ASSIGNMENT)
                node.identifier = identifierNode
                node.expression = make_expression_node(tokenized_line[1:])
                ast_nodes.append(node)

        elif tokenized_line[0].token_type == Token.TOKEN_TYPE.IF:
            node = ASTNode(ASTNode.NodeType.IF)
            node.expression = make_expression_node(tokenized_line[1:])
            ast_nodes.append(node)
            
        elif tokenized_line[0].token_type == Token.TOKEN_TYPE.ELIF:
            node = ASTNode(ASTNode.NodeType.ELIF)
            node.expression = make_expression_node(tokenized_line[1:])
            ast_nodes.append(node)

        elif tokenized_line[0].token_type == Token.TOKEN_TYPE.ELSE:
            node = ASTNode(ASTNode.NodeType.ELSE)
            ast_nodes.append(node)

        elif tokenized_line[0].token_type == Token.TOKEN_TYPE.RETURN:
            node = ASTNode(ASTNode.NodeType.RETURN)
            node.expression = make_expression_node(tokenized_line[1:])
            ast_nodes.append(node)

        elif tokenized_line[0].token_type == Token.TOKEN_TYPE.WHILE:
            node = ASTNode(ASTNode.NodeType.WHILE)
            node.expression = make_expression_node(tokenized_line[1:])
            ast_nodes.append(node)

        elif tokenized_line[0].token_type == Token.TOKEN_TYPE.END:
            node = ASTNode(ASTNode.NodeType.END)
            ast_nodes.append(node)

    print(" -- CODE GENERATION -- ")
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
                else:
                    print(testing_node.nodeType)
                    expression += write_expression(testing_node)

                return expression

            expression = ""
            if node.nodeType == ASTNode.NodeType.LITERAL:
                expression += node.value;
            elif node.nodeType == ASTNode.NodeType.IDENTIFIER:
                expression += node.name;

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

        elif node.nodeType == node.NodeType.FUNCTION_CALL:
            if node.identifier == None:
                raise SyntaxError("Null Identifier")

            identifier = node.identifier.name
            args = node.args
            my_code.append(f"{get_block()}{identifier}({', '.join([write_expression(arg) for arg in args])})")

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

    with open("mycode.py", "w+") as f:
        for line in my_code:
            f.write(line + "\n")


main()
