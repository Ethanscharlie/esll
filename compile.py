from enum import Enum

class TokenType(Enum):
    KEYWORD = 0
    IDENTIFIER = 1
    OPERATOR = 2
    LITERAL = 3

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
        for c in line:
            added_to_word = False

            if in_quotes:
                tokenized_lines[-1][-1].value += c

                if c == "\"":
                    in_quotes = False
                    continue

            elif c == " ":
                pass

            elif c == "=":
                tokenized_lines[-1].append(Token(TokenType.OPERATOR, "="))

            elif c == "(":
                tokenized_lines[-1].append(Token(TokenType.OPERATOR, "("))

            elif c == ")":
                tokenized_lines[-1].append(Token(TokenType.OPERATOR, ")"))

            elif c == ":":
                tokenized_lines[-1].append(Token(TokenType.OPERATOR, ":"))

            elif c == "\"":
                in_quotes = True
                tokenized_lines[-1].append(Token(TokenType.LITERAL, "\""))

            else: 
                added_to_word = True
                word_collecter += c

            if not added_to_word and len(word_collecter) > 0:
                tokenized_lines[-1].insert(-1, Token(TokenType.IDENTIFIER, word_collecter))
                word_collecter = ""

    for tokenized_line in tokenized_lines:
        for token in tokenized_line:
            print(token)


    with open("mycode.py", "w+") as f:
        for line in my_code:
            f.write(line + "\n")


main()
