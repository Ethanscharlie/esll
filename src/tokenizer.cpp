#include "tokenizer.hpp"

#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

const int MAX_TOKENS_PER_LINE = 100;

bool isNumeric(const std::string &str) {
  for (char ch : str) {
    if (ch == '.') {
      continue;
    }
    if (!isdigit(ch)) {
      return false; // Return false if any character is not a digit
    }
  }
  return true; // All characters are digits
}

static Token addWordToken(std::string word) {
  TokenType tokenType = TokenType_IDENTIFIER;

  // Check if it"s a number (integer or float)
  if (isNumeric(word)) {
    tokenType = TokenType_LITERAL;
  }
  // Check if it"s a boolean literal
  else if (word == "false" || word == "true") {
    tokenType = TokenType_LITERAL;
  }
  // Check for specific types
  else if (word == "String" || word == "Integer" || word == "Decimal" ||
           word == "Boolean" || word == "Void") {
    tokenType = TokenType_TYPE;
  }
  // Check for keywords
  else if (word == "if") {
    tokenType = TokenType_IF;
  } else if (word == "while") {
    tokenType = TokenType_WHILE;
  } else if (word == "end") {
    tokenType = TokenType_END;
  } else if (word == "elif") {
    tokenType = TokenType_ELIF;
  } else if (word == "else") {
    tokenType = TokenType_ELSE;
  } else if (word == "return") {
    tokenType = TokenType_RETURN;
  }

  // If it"s still an identifier, prefix it
  if (tokenType == TokenType_IDENTIFIER) {
    word = "esll_" + word;
  }

  return {tokenType, word};
}

std::vector<std::vector<Token>> tokenize(std::vector<std::string> lines) {
  std::vector<std::vector<Token>> tokenizedLines;

  bool inQuotes = false;
  std::string wordCollector = "";

  for (int lineNumber = 0; lineNumber < lines.size(); lineNumber++) {
    std::vector<Token> tokenizedLine;
    const std::string &line = lines[lineNumber];
    int endingCharNumber = 0;

    for (int charNumber = 0; charNumber < line.size(); charNumber++) {
      std::string c(1, line[charNumber]);

      bool addedToWord = false;
      Token token = {TokenType_IDENTIFIER, ""};
      endingCharNumber = charNumber;

      if (inQuotes) {
        tokenizedLine.back().value += c;
        if (c == "\"") {
          inQuotes = false;
          continue;
        }
      }

      else if (c == " ") {
        // Whitespace, no nothing
      } else if (c == ",") {
        token = {TokenType_SEPERATOR, c};
      } else if (c == "+") {
        token = {TokenType_ADD, c};
      } else if (c == "-") {
        token = {TokenType_SUBTRACT, c};
      } else if (c == "*") {
        token = {TokenType_MULTIPLY, c};
      } else if (c == "/") {
        token = {TokenType_DIVIDE, c};
      } else if (c == "%") {
        token = {TokenType_MODULUS, c};
      } else if (c == "&") {
        token = {TokenType_AND, c};
      } else if (c == "|") {
        token = {TokenType_OR, c};
      } else if (c == ">") {
        token = {TokenType_GREATER_THAN, c};
      } else if (c == "<") {
        token = {TokenType_LESS_THAN, c};
      } else if (c == "=") {
        token = {TokenType_EQUALS, c};
      } else if (c == "(") {
        token = {TokenType_OPENING_PARENTHESIS, c};
      } else if (c == ")") {
        token = {TokenType_CLOSING_PARENTHESIS, c};
      } else if (c == "\"") {
        inQuotes = true;
        token = {TokenType_LITERAL, "\""};
      } else {
        addedToWord = true;
        wordCollector += c;
      }

      if (!addedToWord && wordCollector.size() > 0) {
        Token newToken = addWordToken(wordCollector);
        wordCollector = "";
        tokenizedLine.push_back(newToken);
      }

      if (!(token.tokenType == TokenType_IDENTIFIER && token.value == "")) {
        tokenizedLine.push_back(token);
      }
    }

    if (wordCollector.size() > 0) {
      Token newToken = addWordToken(wordCollector);
      wordCollector = "";
      tokenizedLine.push_back(newToken);
    }

    tokenizedLines.push_back(tokenizedLine);
  }
  return tokenizedLines;
}
