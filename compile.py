from __future__ import annotations
from ast import AST, Expression, arguments, expr, operator
from dataclasses import dataclass
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

    nodeType: NodeType

    @dataclass 
    class IDENTIFIER: name: str; esllType: EsllType

    @dataclass
    class LITERAL: value: str; esllType: EsllType

    @dataclass
    class TYPE: esllType: EsllType

    @dataclass
    class ADD: first: ASTNode; second: ASTNode

    @dataclass
    class SUBTRACT: first: ASTNode; second: ASTNode

    @dataclass
    class MULTIPLY: first: ASTNode; second: ASTNode

    @dataclass
    class DIVIDE: first: ASTNode; second: ASTNode

    @dataclass
    class MODULUS: first: ASTNode; second: ASTNode

    @dataclass
    class EQUALS: first: ASTNode; second: ASTNode

    @dataclass
    class GREATER_THAN: first: ASTNode; second: ASTNode

    @dataclass
    class LESS_THAN: first: ASTNode; second: ASTNode

    @dataclass
    class AND: first: ASTNode; second: ASTNode

    @dataclass
    class OR: first: ASTNode; second: ASTNode

    @dataclass
    class VARIABLE_DECLARATION: esllType: EsllType; identifier: ASTNode; expression: ASTNode 

    @dataclass
    class FUNCTION_ARGUMENT_DECLARATION: esllType: EsllType; identifier: ASTNode

    @dataclass
    class FUNCTION_DECLARATION: esllType: EsllType; identifier: ASTNode; arguments: list["ASTNode"]

    @dataclass
    class VARIABLE_ASSIGNMENT: identifier: ASTNode; expression: ASTNode

    @dataclass
    class FUNCTION_CALL: identifier: ASTNode; arguments: list["ASTNode"]

    @dataclass
    class IF: expression: ASTNode

    @dataclass
    class WHILE: expression: ASTNode

    @dataclass
    class END: pass



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
                    data_node.IDENTIFIER.name = data_token.value

                elif data_token.token_type == Token.TOKEN_TYPE.LITERAL:
                    data_node = ASTNode(ASTNode.NodeType.LITERAL)
                    data_node.LITERAL.value = data_token.value

                return data_node

            node = make_data_node(tokens[0])
            for i, token in enumerate(tokens):
                if token.token_type == Token.TOKEN_TYPE.ADD:
                    new_node = ASTNode(ASTNode.NodeType.ADD)
                    new_node.ADD.first = node
                    new_node.ADD.second = make_data_node(tokens[i + 1])
                    node = new_node

                elif token.token_type == Token.TOKEN_TYPE.SUBTRACT:
                    new_node = ASTNode(ASTNode.NodeType.SUBTRACT)
                    new_node.SUBTRACT.first = node
                    new_node.SUBTRACT.second = make_data_node(tokens[i + 1])
                    node = new_node

                elif token.token_type == Token.TOKEN_TYPE.MULTIPLY:
                    new_node = ASTNode(ASTNode.NodeType.MULTIPLY)
                    new_node.MULTIPLY.first = node
                    new_node.MULTIPLY.second = make_data_node(tokens[i + 1])
                    node = new_node

                elif token.token_type == Token.TOKEN_TYPE.DIVIDE:
                    new_node = ASTNode(ASTNode.NodeType.DIVIDE)
                    new_node.DIVIDE.first = node
                    new_node.DIVIDE.second = make_data_node(tokens[i + 1])
                    node = new_node

                elif token.token_type == Token.TOKEN_TYPE.MODULUS:
                    new_node = ASTNode(ASTNode.NodeType.MODULUS)
                    new_node.MODULUS.first = node
                    new_node.MODULUS.second = make_data_node(tokens[i + 1])
                    node = new_node

                elif token.token_type == Token.TOKEN_TYPE.GREATER_THAN:
                    new_node = ASTNode(ASTNode.NodeType.GREATER_THAN)
                    new_node.GREATER_THAN.first = node
                    new_node.GREATER_THAN.second = make_data_node(tokens[i + 1])
                    node = new_node

                elif token.token_type == Token.TOKEN_TYPE.LESS_THAN:
                    new_node = ASTNode(ASTNode.NodeType.LESS_THAN)
                    new_node.LESS_THAN.first = node
                    new_node.LESS_THAN.second = make_data_node(tokens[i + 1])
                    node = new_node
                    
                elif token.token_type == Token.TOKEN_TYPE.EQUALS:
                    new_node = ASTNode(ASTNode.NodeType.EQUALS)
                    new_node.EQUALS.first = node
                    new_node.EQUALS.second = make_data_node(tokens[i + 1])
                    node = new_node
                    
                elif token.token_type == Token.TOKEN_TYPE.OR:
                    new_node = ASTNode(ASTNode.NodeType.OR)
                    new_node.OR.first = node
                    new_node.OR.second = make_data_node(tokens[i + 1])
                    node = new_node

            return node

        node: ASTNode

        if len(tokenized_line) == 0:
            continue

        if tokenized_line[0].token_type == Token.TOKEN_TYPE.TYPE:
            declarationType = tokenized_line[0].value

            if tokenized_line[1].token_type == Token.TOKEN_TYPE.IDENTIFIER:
                identifier = tokenized_line[1].value
                identifierNode = ASTNode(ASTNode.NodeType.IDENTIFIER)
                identifierNode.IDENTIFIER.name = identifier

                if tokenized_line[2].token_type == Token.TOKEN_TYPE.OPENING_PARENTHESIS:
                    pass
                else:
                    node = ASTNode(ASTNode.NodeType.VARIABLE_DECLARATION)
                    node.VARIABLE_DECLARATION.esllType = get_type(declarationType)
                    node.VARIABLE_DECLARATION.identifier = identifierNode
                    node.VARIABLE_DECLARATION.expression = make_expression_node(tokenized_line[2:])
                    ast_nodes.append(node)
            else:
                raise SyntaxError("Identifier expected")

    # PYTHON CODE GENERATION
    for node in ast_nodes:
        def write_expression(node: ASTNode) -> str:
            expression = ""

            def checkNode(testing_node: ASTNode):
                expression = ""

                if testing_node.nodeType == ASTNode.NodeType.LITERAL:
                    expression += testing_node.LITERAL.value;
                elif testing_node.nodeType == ASTNode.NodeType.IDENTIFIER:
                    expression += testing_node.IDENTIFIER.name;
                else:
                    expression += write_expression(testing_node)

                return expression

            if node.nodeType == ASTNode.NodeType.ADD:
                expression += checkNode(node.ADD.first)
                expression += "+"
                expression += checkNode(node.ADD.second)

            return expression
            
        if node.nodeType == node.NodeType.VARIABLE_DECLARATION:
            identifier = node.VARIABLE_DECLARATION.identifier.IDENTIFIER.name
            expression = node.VARIABLE_DECLARATION.expression
            my_code.append(f"{identifier} = {write_expression(expression)}")
            

    my_code.append("main()")

    with open("mycode.py", "w+") as f:
        for line in my_code:
            f.write(line + "\n")


main()
