#include "asttree.hpp"
#include "tokenizer.hpp"
#include <math.h>
#include <memory>
#include <stdexcept>
#include <stdio.h>
#include <string.h>
#include <utility>
#include <vector>

static EsllType getType(const std::string &name) {
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

static std::unique_ptr<ASTNode>
makeExpressionNode(const std::vector<Token> &tokens);

static std::unique_ptr<ASTNode> makeDataNode(const std::vector<Token> &tokens,
                                             int &i) {
  const Token &dataToken = tokens[i];
  auto dataNode = std::make_unique<ASTNode>(NodeType_NONE);

  switch (dataToken.tokenType) {
  case TokenType_IDENTIFIER: {
    auto identifierNode = std::make_unique<ASTNode>(NodeType_IDENTIFIER);
    identifierNode->name = dataToken.value;

    printf("MARKSOMETHINGIDK i: %d, size: %d\n", i, (int)tokens.size());
    if (i < tokens.size() - 1 &&
        tokens[i + 1].tokenType == TokenType_OPENING_PARENTHESIS) {
      dataNode->nodeType = NodeType_FUNCTION_CALL;
      dataNode->identifier = std::move(identifierNode);

      i += 2;

      int parenthesisDeep = 0;
      std::vector<Token> expressionCollector;
      // TODO Broken code found tokens[*i] != TokenType_CLOSING_PARENTHESIS
      while (parenthesisDeep > 0 || true) {
        printf("MARKWHILE %d\n", i);
        const Token &argToken = tokens[i];

        switch (argToken.tokenType) {
        case TokenType_SEPERATOR: {
          dataNode->args.push_back(makeExpressionNode(expressionCollector));
          break;
        }

        case TokenType_OPENING_PARENTHESIS: {
          parenthesisDeep++;
          break;
        }

        case TokenType_CLOSING_PARENTHESIS: {
          parenthesisDeep--;
          break;
        }

        default: {
          expressionCollector.push_back(argToken);
        }
        }

        i++;
        if (i == tokens.size()) {
          i -= 2;
          break;
        }
      }

      i += 1;
      printf("MARK %d\n", (int)expressionCollector.size());
      dataNode->args.push_back(makeExpressionNode(expressionCollector));
    } else { // Is a variable
      dataNode = std::move(identifierNode);
    }
  } break;

  case TokenType_LITERAL: {
    dataNode->nodeType = NodeType_LITERAL;
    dataNode->value = dataToken.value;
  } break;
  }

  return std::move(dataNode);
}

static std::vector<Token> chopOffBeg(const std::vector<Token> &tokens,
                                     int chop) {
  std::vector<Token> chopedTokens;

  for (int i = chop; i < tokens.size(); i++) {
    chopedTokens.push_back(tokens[i]);
  }

  return chopedTokens;
}

static std::unique_ptr<ASTNode>
makeExpressionNode(const std::vector<Token> &tokens) {
  int i = 0;
  std::unique_ptr<ASTNode> node = makeDataNode(tokens, i);

  while (i < tokens.size()) {
    const Token *token = &tokens[i];

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

  return std::move(node);
}

static std::unique_ptr<ASTNode>
makeArgDecNode(const std::vector<Token> &argCollector) {
  if (argCollector.size() != 2) {
    throw std::runtime_error("Argument Definition has an extra token");
  } else if (argCollector[0].tokenType != TokenType_TYPE) {
    throw std::runtime_error("Type expected on argument definition");
  } else if (argCollector[1].tokenType != TokenType_IDENTIFIER) {
    throw std::runtime_error("Identifier expected on argument definition");
  }

  auto newArgNode =
      std::make_unique<ASTNode>(NodeType_FUNCTION_ARGUMENT_DECLARATION);
  newArgNode->esllType = getType(argCollector[0].value);
  newArgNode->identifier = std::make_unique<ASTNode>(NodeType_IDENTIFIER);
  newArgNode->identifier->name = argCollector[1].value;

  return std::move(newArgNode);
}

std::vector<std::unique_ptr<ASTNode>>
generateASTTree(std::vector<std::vector<Token>> tokenizedLines) {
  std::vector<std::unique_ptr<ASTNode>> astNodes;

  for (int i = 0; i < tokenizedLines.size(); i++) {
    std::vector<Token> line = tokenizedLines[i];

    std::unique_ptr<ASTNode> node = std::make_unique<ASTNode>(NodeType_NONE);

    if (line.size() == 0) {
      continue;
    }

    switch (line[0].tokenType) {
    case TokenType_TYPE: {
      std::string declarationType = line[0].value;

      if (line[1].tokenType == TokenType_IDENTIFIER) {
        std::string identifier = line[1].value;
        std::unique_ptr<ASTNode> identifierNode =
            std::make_unique<ASTNode>(NodeType_IDENTIFIER);
        identifierNode->name = identifier;

        if (line[2].tokenType == TokenType_OPENING_PARENTHESIS) {
          node->nodeType = NodeType_FUNCTION_DECLARATION;
          node->esllType = getType(declarationType);
          node->identifier = std::move(identifierNode);

          std::vector<Token> argCollector;
          for (int argTokenIndex = 3; argTokenIndex < line.size() - 1;
               argTokenIndex++) {
            const Token &argToken = line[argTokenIndex];

            if (argToken.tokenType == TokenType_SEPERATOR) {
              node->args.push_back(makeArgDecNode(argCollector));
              argCollector.clear();
            } else {
              argCollector.push_back(argToken);
            }
          }

          if (argCollector.size() > 0) {
            node->args.push_back(makeArgDecNode(argCollector));
          }

          astNodes.push_back(std::move(node));
        } else {
          node->nodeType = NodeType_VARIABLE_DECLARATION;
          node->esllType = getType(declarationType);
          node->identifier = std::move(identifierNode);

          std::unique_ptr<ASTNode> expressionNode =
              makeExpressionNode(chopOffBeg(line, 2));
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
        astNodes.push_back(makeExpressionNode(line));
      } else {
        auto node = std::make_unique<ASTNode>(NodeType_VARIABLE_ASSIGNMENT);
        node->identifier = std::move(identifierNode);

        std::unique_ptr<ASTNode> expressionNode =
            makeExpressionNode(chopOffBeg(line, 1));
        node->expression = std::move(expressionNode);

        astNodes.push_back(std::move(node));
      }
    } break;

    case TokenType_IF: {
      node->nodeType = NodeType_IF;
      node->expression = std::move(makeExpressionNode(chopOffBeg(line, 1)));
      astNodes.push_back(std::move(node));
    } break;

    case TokenType_ELIF: {
      node->nodeType = NodeType_ELIF;
      node->expression = std::move(makeExpressionNode(chopOffBeg(line, 1)));
      astNodes.push_back(std::move(node));
    } break;

    case TokenType_ELSE: {
      node->nodeType = NodeType_ELSE;
      astNodes.push_back(std::move(node));
    } break;

    case TokenType_RETURN: {
      node->nodeType = NodeType_RETURN;
      node->expression = std::move(makeExpressionNode(chopOffBeg(line, 1)));
      astNodes.push_back(std::move(node));
    } break;

    case TokenType_WHILE: {
      node->nodeType = NodeType_WHILE;
      node->expression = std::move(makeExpressionNode(chopOffBeg(line, 1)));
      astNodes.push_back(std::move(node));
    } break;

    case TokenType_END: {
      node->nodeType = NodeType_END;
      astNodes.push_back(std::move(node));
    } break;
    }
  }

  return astNodes;
}
