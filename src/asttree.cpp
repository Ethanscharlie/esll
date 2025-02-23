#include "asttree.hpp"
#include "tokenizer.hpp"
#include <iostream>
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

void ASTNode::print(const int &level) {
  std::string nodeTypeText;

  switch (nodeType) {
  case NodeType_NONE:
    nodeTypeText = "None";
    break;
  case NodeType_IDENTIFIER:
    nodeTypeText = "Identifier";
    break;
  case NodeType_LITERAL:
    nodeTypeText = "Literal";
    break;
  case NodeType_TYPE:
    nodeTypeText = "Type";
    break;

  case NodeType_ADD:
    nodeTypeText = "Add";
    break;
  case NodeType_SUBTRACT:
    nodeTypeText = "Subtract";
    break;
  case NodeType_MULTIPLY:
    nodeTypeText = "Mulitply";
    break;
  case NodeType_DIVIDE:
    nodeTypeText = "Divide";
    break;
  case NodeType_MODULUS:
    nodeTypeText = "Modulus";
    break;

  case NodeType_EQUALS:
    nodeTypeText = "Equals";
    break;
  case NodeType_GREATER_THAN:
    nodeTypeText = "Greater Than";
    break;
  case NodeType_LESS_THAN:
    nodeTypeText = "Less Than";
    break;
  case NodeType_AND:
    nodeTypeText = "And";
    break;
  case NodeType_OR:
    nodeTypeText = "Or";
    break;

  case NodeType_VARIABLE_DECLARATION:
    nodeTypeText = "Variable Declaration";
    break;
  case NodeType_FUNCTION_DECLARATION:
    nodeTypeText = "Variable Declaration";
    break;
  case NodeType_VARIABLE_ASSIGNMENT:
    nodeTypeText = "Variable Assignment";
    break;
  case NodeType_FUNCTION_CALL:
    nodeTypeText = "Function Call";
    break;

  case NodeType_FUNCTION_ARGUMENT_DECLARATION:
    nodeTypeText = "Function Argument Declaration";
    break;

  case NodeType_IF:
    nodeTypeText = "If";
    break;
  case NodeType_WHILE:
    nodeTypeText = "While";
    break;
  case NodeType_END:
    nodeTypeText = "End";
    break;
  case NodeType_ELIF:
    nodeTypeText = "Elif";
    break;
  case NodeType_ELSE:
    nodeTypeText = "Else";
    break;
  case NodeType_RETURN:
    nodeTypeText = "Return";
    break;
  }
  std::cout << "NodeType: [" << nodeTypeText << "], Value: [" << value
            << "], Name: [" << name << "], esllType: [" << esllType << "]\n";

  auto indent = [level]() {
    for (int i = 0; i < level; i++) {
      std::cout << "   ";
    }
  };

  if (first != nullptr) {
    indent();
    std::cout << "first: ";
    first->print(level + 1);
  }
  if (second != nullptr) {
    indent();
    std::cout << "second: ";
    second->print(level + 1);
  }
  if (identifier != nullptr) {
    indent();
    std::cout << "id: ";
    identifier->print(level + 1);
  }
  if (expression != nullptr) {
    indent();
    std::cout << "expression: ";
    expression->print(level + 1);
  }
  if (args.size() > 0) {
    indent();
    std::cout << "args\n";
    for (const auto &arg : args) {
      indent();
      std::cout << "  arg: \n";
      arg->print(level + 1);
    }
  }
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

    if (i < tokens.size() - 1 &&
        tokens[i + 1].tokenType == TokenType_OPENING_PARENTHESIS) {
      dataNode->nodeType = NodeType_FUNCTION_CALL;
      dataNode->identifier = std::move(identifierNode);

      i += 2;

      int parenthesisDeep = 0;
      std::vector<Token> expressionCollector;
      // TODO Broken code found tokens[*i] != TokenType_CLOSING_PARENTHESIS
      while (parenthesisDeep > 0 || true) {
        const Token &argToken = tokens[i];

        switch (argToken.tokenType) {
        case TokenType_SEPERATOR: {
          dataNode->args.push_back(makeExpressionNode(expressionCollector));
          expressionCollector.clear();
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
      auto newNode = std::make_unique<ASTNode>(NodeType_SUBTRACT);
      newNode->first = std::move(node);

      // Negitive Numbers

      i++;
      std::unique_ptr<ASTNode> secondNode = makeDataNode(tokens, i);
      newNode->second = std::move(secondNode);
      node = std::move(newNode);
    } break;

    case TokenType_MULTIPLY: {
      auto newNode = std::make_unique<ASTNode>(NodeType_MULTIPLY);
      newNode->first = std::move(node);
      i++;
      std::unique_ptr<ASTNode> secondNode = makeDataNode(tokens, i);
      newNode->second = std::move(secondNode);
      node = std::move(newNode);
    } break;

    case TokenType_DIVIDE: {
      auto newNode = std::make_unique<ASTNode>(NodeType_DIVIDE);
      newNode->first = std::move(node);
      i++;
      std::unique_ptr<ASTNode> secondNode = makeDataNode(tokens, i);
      newNode->second = std::move(secondNode);
      node = std::move(newNode);
    } break;

      // break;
    case TokenType_MODULUS: {
      auto newNode = std::make_unique<ASTNode>(NodeType_MODULUS);
      newNode->first = std::move(node);
      i++;
      std::unique_ptr<ASTNode> secondNode = makeDataNode(tokens, i);
      newNode->second = std::move(secondNode);
      node = std::move(newNode);
    } break;

    case TokenType_GREATER_THAN: {
      auto newNode = std::make_unique<ASTNode>(NodeType_GREATER_THAN);
      newNode->first = std::move(node);
      i++;
      std::unique_ptr<ASTNode> secondNode = makeDataNode(tokens, i);
      newNode->second = std::move(secondNode);
      node = std::move(newNode);
    } break;

    case TokenType_LESS_THAN: {
      auto newNode = std::make_unique<ASTNode>(NodeType_LESS_THAN);
      newNode->first = std::move(node);
      i++;
      std::unique_ptr<ASTNode> secondNode = makeDataNode(tokens, i);
      newNode->second = std::move(secondNode);
      node = std::move(newNode);
    } break;

    case TokenType_EQUALS: {
      auto newNode = std::make_unique<ASTNode>(NodeType_EQUALS);
      newNode->first = std::move(node);
      i++;
      std::unique_ptr<ASTNode> secondNode = makeDataNode(tokens, i);
      newNode->second = std::move(secondNode);
      node = std::move(newNode);
    } break;

    case TokenType_OR: {
      auto newNode = std::make_unique<ASTNode>(NodeType_OR);
      newNode->first = std::move(node);
      i++;
      std::unique_ptr<ASTNode> secondNode = makeDataNode(tokens, i);
      newNode->second = std::move(secondNode);
      node = std::move(newNode);
    } break;

    case TokenType_AND: {
      auto newNode = std::make_unique<ASTNode>(NodeType_AND);
      newNode->first = std::move(node);
      i++;
      std::unique_ptr<ASTNode> secondNode = makeDataNode(tokens, i);
      newNode->second = std::move(secondNode);
      node = std::move(newNode);
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
