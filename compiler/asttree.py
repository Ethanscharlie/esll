from __future__ import annotations

from globals import EsllType
from tokenizer import Token
from dataclasses import dataclass, field
from enum import Enum

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

def generate_ast_tree(tokenized_lines: list[list[Token]]) -> list[ASTNode]:
    ast_nodes: list[ASTNode] = []

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

    return ast_nodes

