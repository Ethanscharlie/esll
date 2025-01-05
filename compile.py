from ast import expr, operator
from enum import Enum
from os import confstr, walk

valid_types = [
    "Void",
    "Integer",
    "Decimal",
    "Boolean",
    "String"
]

valid_keywords = [
    "end",
    "if",
    "while",
    "else",
    "elif",
    "return"
]

valid_operators = [
    "=",
    "+",
    "-",
    "/",
    "*",
    "(",
    ")",
    "%",
    ">",
    "<",
    "&",
    "|"
]

variable_tracker: dict[str, str] = {}

class TokenType(Enum):
    KEYWORD = 0
    IDENTIFIER = 1
    OPERATOR = 2
    LITERAL = 3
    TYPE = 4
    SEPERATOR = 5

class Token:
    def __init__(self, token_type: TokenType, value: str):
        self.token_type = token_type
        self.value = value

    def __repr__(self) -> str:
        return f"Type: {self.token_type}, Value: {self.value}"

def compile_expression(tokens: list[Token]) -> str:
    expression = ""

    for token in tokens:
        if token.token_type == TokenType.IDENTIFIER:
            expression += token.value

        elif token.token_type == TokenType.LITERAL:
            literal = token.value

            # Boolean to python boolean
            if literal == "true": literal = "True"
            elif literal == "false": literal = "False"

            expression += literal

        elif token.token_type == TokenType.OPERATOR:
            operator = token.value
            if operator == "&": operator = " and "
            if operator == "|": operator = " or "
            if operator == "=": operator = "=="

            expression += operator

    return expression


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
            token_type = TokenType.IDENTIFIER

            if word.replace(".", "").isnumeric():
                token_type = TokenType.LITERAL

            if word == "false" or word == "true":
                token_type = TokenType.LITERAL

            elif word.replace("#", "") in valid_types:
                token_type = TokenType.TYPE

            elif word in valid_keywords:
                token_type = TokenType.KEYWORD

            tokenized_lines[-1].append(Token(token_type, word))

        for i in range(len(line)):
            c = line[i]

            added_to_word = False
            token = Token(TokenType.IDENTIFIER, "")

            if in_quotes:
                tokenized_lines[-1][-1].value += c

                if c == "\"":
                    in_quotes = False
                    continue

            elif c == " ":
                pass

            elif c == ",":
                token = Token(TokenType.SEPERATOR, c)

            elif c in valid_operators:
                token = Token(TokenType.OPERATOR, c)

            elif c == "\"":
                in_quotes = True
                token = Token(TokenType.LITERAL, "\"")

            else: 
                added_to_word = True
                word_collecter += c

            if not added_to_word and len(word_collecter) > 0:
                add_word_token(word_collecter)
                word_collecter = ""

            if not (token.token_type == TokenType.IDENTIFIER and token.value == ""):
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

    block = 0
    index = 0
    for tokenized_line in tokenized_lines:
        index += 1
        print("On Line: " + str(index))

        def block_text() -> str:
            return "    " * block

        if len(tokenized_line) == 0:
            continue

        if tokenized_line[0].token_type == TokenType.IDENTIFIER: # Must be setting a variable or calling a function
            identifier = tokenized_line[0].value

            if tokenized_line[1].token_type == TokenType.OPERATOR:
                para = 0
                if tokenized_line[1].value == "(":
                    args: list[str] = [""]
                    i = 2
                    while tokenized_line[i].value != ")" or para != 0:
                        if tokenized_line[i].token_type == TokenType.SEPERATOR:
                            args.append("")
                            i += 1
                            continue

                        if tokenized_line[i].value == "(":
                            para += 1

                        token = tokenized_line[i]

                        if para > 0:
                            args[-1] += str(token.value)
                        else:
                            args[-1] += str(token.value)

                        if tokenized_line[i].value == ")":
                            para -= 1

                        i += 1

                    my_code.append(f"{block_text()}{tokenized_line[0].value}({', '.join(args)})")

            else: # Variable
                expression = compile_expression(tokenized_line[1:])
                my_code.append(f"{block_text()}{identifier} = {expression}")
        
        elif tokenized_line[0].token_type == TokenType.TYPE: # Defining a variable or a function
            definition_type = tokenized_line[0]
            if tokenized_line[1].token_type == TokenType.IDENTIFIER:
                identifier = tokenized_line[1].value

                if len(tokenized_line) > 2 and tokenized_line[2].token_type == TokenType.OPERATOR: 
                    if tokenized_line[2].value == "(":
                        new_function_args: list[str] = []
                        for i in range(2, len(tokenized_line)):
                            if tokenized_line[i].token_type == TokenType.IDENTIFIER:
                                new_function_args.append(tokenized_line[i].value)

                        # Fuck args for now
                        my_code.append(f"{block_text()}def {identifier}({', '.join(new_function_args)}):")
                        block += 1
                else:
                    variable_tracker[identifier] = definition_type.value

                    if definition_type.value[-1] == "#":
                        my_code.append(f"{block_text()}{identifier} = []")
                    else:
                        expression = compile_expression(tokenized_line[2:])
                        my_code.append(f"{block_text()}{identifier} = {expression}")


        elif tokenized_line[0].token_type == TokenType.KEYWORD:
            if tokenized_line[0].value == "end":
                if block == 0:
                    raise SyntaxError(f"Line: {len(my_code)}, Misplaced end keyword")
                block -= 1

            elif tokenized_line[0].value == "if":
                expression = compile_expression(tokenized_line[1:])
                my_code.append(f"{block_text()}if ({expression}):")
                block += 1

            elif tokenized_line[0].value == "while":
                expression = compile_expression(tokenized_line[1:])
                my_code.append(f"{block_text()}while ({expression}):")
                block += 1

            elif tokenized_line[0].value == "return":
                expression = compile_expression(tokenized_line[1:])
                my_code.append(f"{block_text()}return {expression}")

            elif tokenized_line[0].value == "elif":
                block -= 1
                expression = compile_expression(tokenized_line[1:])
                my_code.append(f"{block_text()}elif ({expression}):")
                block += 1

            elif tokenized_line[0].value == "else":
                block -= 1
                my_code.append(f"{block_text()}else:")
                block += 1

    my_code.append("main()")

    with open("mycode.py", "w+") as f:
        for line in my_code:
            f.write(line + "\n")


main()
