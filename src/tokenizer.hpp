#pragma once
#include <string>
#include <vector>
extern const int MAX_TOKENS_PER_LINE;

enum TokenType {
  TokenType_IDENTIFIER,
  TokenType_LITERAL,
  TokenType_TYPE,

  TokenType_ADD,
  TokenType_SUBTRACT,
  TokenType_MULTIPLY,
  TokenType_DIVIDE,
  TokenType_MODULUS,

  TokenType_EQUALS,
  TokenType_GREATER_THAN,
  TokenType_LESS_THAN,
  TokenType_AND,
  TokenType_OR,

  TokenType_IF,
  TokenType_WHILE,
  TokenType_END,
  TokenType_ELIF,
  TokenType_ELSE,
  TokenType_RETURN,

  TokenType_OPENING_PARENTHESIS,
  TokenType_CLOSING_PARENTHESIS,
  TokenType_SEPERATOR
};

struct Token {
  TokenType tokenType;
  std::string value;
};

std::vector<std::vector<Token>> tokenize(std::vector<std::string> lines);
