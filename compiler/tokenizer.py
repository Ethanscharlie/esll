from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

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

def tokenize(lines: list[str]) -> list[list[Token]]:
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

            # If it's still an identiter we want to add a prefix to it
            if token_type == Token.TOKEN_TYPE.IDENTIFIER:
                word = f"esll_{word}"

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

    return tokenized_lines

