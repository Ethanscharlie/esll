#include "asttree.hpp"
#include "tokenizer.hpp"
#include <math.h>
#include <memory>
#include <stdio.h>
#include <string.h>
#include <utility>
#include <vector>

static EsllType getType(const std::string name) {
  if (name == "String") {
    return EsllType_STRING;
  } else if (name == "Integer") {
    return EsllType_INTEGER;
  } else if (name == "Decimal") {
    return EsllType_DECIMAL;
  } else if (name == "Void") {
    return EsllType_VOID;
  } else if (name == "Boolean") {
    return EsllType_BOOLEAN;
  }

  return EsllType_VOID;
}

static std::unique_ptr<ASTNode> makeExpressionNode(std::vector<Token> tokens,
                                                   int *i);

static std::unique_ptr<ASTNode> makeDataNode(std::vector<Token> tokens,
                                             int *i) {
  Token dataToken = tokens[*i];
  std::unique_ptr<ASTNode> dataNode = std::make_unique<ASTNode>(NodeType_NONE);

  switch (dataToken.tokenType) {
  case TokenType_IDENTIFIER: {
    std::unique_ptr<ASTNode> identifierNode =
        std::make_unique<ASTNode>(NodeType_IDENTIFIER);
    identifierNode->name = dataToken.value;

    if (*i < tokens.size() - 1 &&
        tokens[*i + 1].tokenType == TokenType_OPENING_PARENTHESIS) {
      dataNode->nodeType = NodeType_FUNCTION_CALL;
      dataNode->identifier = std::move(identifierNode);

      i += 2;

      int parenthesisDeep = 0;
      std::vector<Token> expressionCollector;
      int expressionCollectorSize = 0;
      // TODO Broken code found tokens[*i] != TokenType_CLOSING_PARENTHESIS
      while (parenthesisDeep > 0) {
        Token argToken = tokens[*i];

        switch (argToken.tokenType) {
        case TokenType_SEPERATOR: {
          std::unique_ptr<ASTNode> newNode =
              makeExpressionNode(expressionCollector, i);
          dataNode->args.push_back(std::move(newNode));
          expressionCollectorSize = 0;
        } break;

        case TokenType_OPENING_PARENTHESIS: {
          parenthesisDeep++;
        } break;

        case TokenType_CLOSING_PARENTHESIS: {
          parenthesisDeep--;
        } break;

        default: {
          expressionCollector[expressionCollectorSize] = argToken;
          expressionCollectorSize++;
        } break;
        }

        i++;
        if (*i == tokens.size()) {
          i -= 2;
          break;
        }
      }
    } else { // Is a variable
      dataNode = std::move(identifierNode);
    }
  } break;

  case TokenType_LITERAL: {
    dataNode->nodeType = NodeType_LITERAL;
    dataNode->value = dataToken.value;
  } break;
  }

  return dataNode;
}

static std::vector<Token> chopOffBeg(std::vector<Token> tokens, int chop) {
  std::vector<Token> chopedTokens;

  for (int i = chop; i < tokens.size(); i++) {
    chopedTokens.push_back(tokens[i]);
  }

  return chopedTokens;
}

static std::unique_ptr<ASTNode> makeExpressionNode(std::vector<Token> tokens,
                                                   int *i) {
  std::unique_ptr<ASTNode> node = makeDataNode(tokens, i);

  while (*i < tokens.size()) {
    Token *token = &tokens[*i];

    switch (token->tokenType) {
    case TokenType_ADD: {
      auto newNode = std::make_unique<ASTNode>(NodeType_ADD);
      newNode->first = std::move(node);
      i++;
      std::unique_ptr<ASTNode> secondNode = makeDataNode(tokens, i);
      newNode->second = std::move(secondNode);
      node = std::move(newNode);
    } break;

    case TokenType_SUBTRACT: {
    } break;

    case TokenType_MULTIPLY: {
    } break;

    case TokenType_DIVIDE: {
    } break;

      break;
    case TokenType_MODULUS: {
    } break;

    case TokenType_GREATER_THAN: {
    } break;

    case TokenType_LESS_THAN: {
    } break;

    case TokenType_EQUALS: {
    } break;

    case TokenType_OR: {
    } break;

    case TokenType_AND: {
    } break;
    }

    i++;
  }

  return node;
}

std::vector<std::unique_ptr<ASTNode>>
generateASTTree(std::vector<std::vector<Token>> tokenizedLines) {
  std::vector<std::unique_ptr<ASTNode>> astNodes;

  for (int i = 0; i < tokenizedLines.size(); i++) {
    std::vector<Token> line = tokenizedLines[i];

    std::unique_ptr<ASTNode> node = std::make_unique<ASTNode>(NodeType_NONE);

    // TODO Check if line is empty

    switch (line[0].tokenType) {
    case TokenType_TYPE: {
      std::string declarationType = line[0].value;

      if (line[1].tokenType == TokenType_IDENTIFIER) {
        std::string identifier = line[1].value;
        std::unique_ptr<ASTNode> identifierNode =
            std::make_unique<ASTNode>(NodeType_IDENTIFIER);
        identifierNode->name = identifier;

        if (line[2].tokenType == TokenType_OPENING_PARENTHESIS) {
          std::unique_ptr<ASTNode> node =
              std::make_unique<ASTNode>(NodeType_FUNCTION_DECLARATION);
          node->esllType = getType(declarationType);
          node->identifier = std::move(identifierNode);

          // TODO arg collector
        } else {
          std::unique_ptr<ASTNode> node =
              std::make_unique<ASTNode>(NodeType_VARIABLE_DECLARATION);
          node->esllType = getType(declarationType);
          node->identifier = std::move(identifierNode);

          int i = 0;
          std::unique_ptr<ASTNode> expressionNode =
              makeExpressionNode(chopOffBeg(line, 2), &i);
          node->expression = std::move(expressionNode);

          astNodes.push_back(std::move(node));
        }
      } else {
        printf("ERROR Identifier Expected\n");
      }
    } break;

    case TokenType_IDENTIFIER: {
      std::string identifier = line[0].value;
      std::unique_ptr<ASTNode> identifierNode =
          std::make_unique<ASTNode>(NodeType_IDENTIFIER);
      identifierNode->name = identifier;

      if (line[1].tokenType == TokenType_OPENING_PARENTHESIS) {
        // astNodes[i] = makeDataNode(line, size, 0);
      } else {
        std::unique_ptr<ASTNode> node =
            std::make_unique<ASTNode>(NodeType_VARIABLE_ASSIGNMENT);
        node->identifier = std::move(identifierNode);

        int i = 0;
        std::unique_ptr<ASTNode> expressionNode =
            makeExpressionNode(chopOffBeg(line, 1), &i);
        node->expression = std::move(expressionNode);

        astNodes.push_back(std::move(node));
      }
    } break;

    case TokenType_IF: {
      node->nodeType = NodeType_IF;
    } break;

    case TokenType_ELIF: {
    } break;

    case TokenType_ELSE: {
    } break;

    case TokenType_RETURN: {
    } break;

    case TokenType_WHILE: {
    } break;

    case TokenType_END: {
    } break;
    }
  }

  return astNodes;
}
