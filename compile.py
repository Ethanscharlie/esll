from ast import operator
from enum import Enum

valid_types = [
    "Void",
    "Integer",
    "String"
]

valid_keywords = [
    "end"
]

class TokenType(Enum):
    KEYWORD = 0
    IDENTIFIER = 1
    OPERATOR = 2
    LITERAL = 3
    TYPE = 4

class Token:
    def __init__(self, token_type: TokenType, value: str):
        self.token_type = token_type
        self.value = value

    def __repr__(self) -> str:
        return f"Type: {self.token_type}, Value: {self.value}"

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

            if word in valid_types:
                token_type = TokenType.TYPE

            if word in valid_keywords:
                token_type = TokenType.KEYWORD

            tokenized_lines[-1].append(Token(token_type, word))

        for c in line:
            added_to_word = False
            token = Token(TokenType.IDENTIFIER, "")

            if in_quotes:
                tokenized_lines[-1][-1].value += c

                if c == "\"":
                    in_quotes = False
                    continue

            elif c == " ":
                pass

            elif c == "=":
                token = Token(TokenType.OPERATOR, "=")

            elif c == "(":
                token = Token(TokenType.OPERATOR, "(")

            elif c == ")":
                token = Token(TokenType.OPERATOR, ")")

            elif c == ":":
                token = Token(TokenType.OPERATOR, ":")

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

    block = 0
    for tokenized_line in tokenized_lines:
        block_text = "    " * block

        if len(tokenized_line) == 0:
            continue

        if tokenized_line[0].token_type == TokenType.IDENTIFIER: # Must be setting a variable or calling a function
            if tokenized_line[1].token_type == TokenType.OPERATOR:
                if tokenized_line[1].value == "=": # Is setting a variable
                    pass
                if tokenized_line[1].value == "(":
                    args: list[str] = []
                    i = 2
                    while tokenized_line[i].value != ")" and tokenized_line[i].token_type != TokenType.OPERATOR:
                        token = tokenized_line[i]
                        args.append(str(token.value))
                        i += 1

                    my_code.append(f"{block_text}{tokenized_line[0].value}({', '.join(args)})")
        
        elif tokenized_line[0].token_type == TokenType.TYPE: # Defining a variable or a function
            definition_type = tokenized_line[0]
            if tokenized_line[1].token_type == TokenType.IDENTIFIER:
                identifier = tokenized_line[1].value

                if tokenized_line[2].token_type == TokenType.OPERATOR: 
                    if tokenized_line[2].value == "=": # Is defining a variable
                        if tokenized_line[3].token_type == TokenType.LITERAL:
                            literal = tokenized_line[3].value

                            my_code.append(f"{block_text}{identifier} = {literal}")

                    elif tokenized_line[2].value == "(":
                        # Fuck args for now
                        my_code.append(f"{block_text}def {identifier}():")
                        block += 1

        elif tokenized_line[0].token_type == TokenType.KEYWORD:
            if tokenized_line[0].value == "end":
                if block == 0:
                    print("Misplaced end keyword")
                block -= 1

    my_code.append("main()")

    with open("mycode.py", "w+") as f:
        for line in my_code:
            f.write(line + "\n")


main()
