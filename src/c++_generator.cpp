#include "asttree.hpp"
#include <format>
#include <stdexcept>
#include <string>
#include <vector>

static std::string typeToCType(const EsllType &esllType) {
  switch (esllType) {
  case EsllType_STRING:
    return "std::string";

  case EsllType_INTEGER:
    return "int";

  case EsllType_DECIMAL:
    return "float";

  case EsllType_VOID:
    return "void";

  case EsllType_BOOLEAN:
    return "bool";
  }

  return "ERRORTYPENOTFOUND";
}

static std::string writeExpression(const ASTNode &node);

static std::string checkNode(ASTNode *testingNode) {
  if (!testingNode) {
    throw std::runtime_error("Node was Null");
  }

  std::string expression = "";
  switch (testingNode->nodeType) {
  case NodeType_LITERAL: {
    expression += testingNode->value;
  } break;

  case NodeType_IDENTIFIER: {
    expression += testingNode->name;
  } break;

  case NodeType_FUNCTION_CALL: {
    if (!testingNode->identifier) {
      throw std::runtime_error("Null Identifier");
    }
    std::string identifier = testingNode->identifier->name;

    const auto &args = testingNode->args;
    expression += identifier;
    expression += "(";
    for (const auto &arg : args) {
      expression += writeExpression(*arg.get());
      if (arg != args.back()) {
        expression += ", ";
      }
    }
    expression += ")";
  } break;
  default: {
    expression += writeExpression(*testingNode);
  }
  }

  return expression;
}

static std::string writeExpression(const ASTNode &node) {
  std::string expression = "";

  switch (node.nodeType) {
  case NodeType_LITERAL: {
    expression += node.value;
  } break;

  case NodeType_IDENTIFIER: {
    expression += node.name;
  } break;

  case NodeType_FUNCTION_CALL: {
    if (!node.identifier) {
      throw std::runtime_error("Null Identifier");
    }
    std::string identifier = node.identifier->name;

    expression += identifier;
    expression += "(";
    for (const std::unique_ptr<ASTNode> &arg : node.args) {
      expression += writeExpression(*arg.get());
      if (arg != node.args.back()) {
        expression += ", ";
      }
    }
    expression += ")";
  } break;

  case NodeType_ADD: {
    expression += checkNode(node.first.get());
    expression += "+";
    expression += checkNode(node.second.get());
  } break;

  case NodeType_SUBTRACT: {
    expression += checkNode(node.first.get());
    expression += "-";
    expression += checkNode(node.second.get());
  } break;

  case NodeType_MULTIPLY: {
    expression += checkNode(node.first.get());
    expression += "*";
    expression += checkNode(node.second.get());
  } break;

  case NodeType_DIVIDE: {
    expression += checkNode(node.first.get());
    expression += "/";
    expression += checkNode(node.second.get());
  } break;

  case NodeType_MODULUS: {
    expression += checkNode(node.first.get());
    expression += "%";
    expression += checkNode(node.second.get());
  } break;

  case NodeType_EQUALS: {
    expression += checkNode(node.first.get());
    expression += "==";
    expression += checkNode(node.second.get());
  } break;

  case NodeType_GREATER_THAN: {
    expression += checkNode(node.first.get());
    expression += ">";
    expression += checkNode(node.second.get());
  } break;

  case NodeType_LESS_THAN: {
    expression += checkNode(node.first.get());
    expression += "<";
    expression += checkNode(node.second.get());
  } break;

  case NodeType_AND: {
    expression += checkNode(node.first.get());
    expression += "&&";
    expression += checkNode(node.second.get());
  } break;

  case NodeType_OR: {
    expression += checkNode(node.first.get());
    expression += "||";
    expression += checkNode(node.second.get());
  } break;
  }

  return expression;
}

std::vector<std::string>
generate_cpp(const std::vector<std::unique_ptr<ASTNode>> &astNodes) {
  std::vector<std::string> myCode;
  myCode.push_back(R"(
// Includes
#include "stdio.h"
#include <stdlib.h>
#include <string>

// Functions
void esll_print(const std::string& text) {
    printf(text.c_str());
    printf("\\n");
}
)");

  int block = 0;
  for (int lineNumber = 0; lineNumber < astNodes.size(); lineNumber++) {
    auto &node = astNodes[lineNumber];

    auto getBlock = [block]() {
      std::string tab;
      for (int i = 0; i < block; i++) {
        tab += "     ";
      }
      return tab;
    };

    switch (node->nodeType) {
    case NodeType_VARIABLE_DECLARATION: {
      if (!node->identifier) {
        throw std::runtime_error("Null Identifier");
      }
      std::string identifier = node->identifier->name;

      const EsllType &esllType = node->esllType;
      const std::string cType = typeToCType(esllType);

      if (!node->expression) {
        throw std::runtime_error("Null Expression");
      }
      const ASTNode &expression = *node->expression;
      const std::string writtenExpression = writeExpression(expression);

      myCode.push_back(std::format("{}{} {} = {};", getBlock(), cType,
                                   identifier, writtenExpression));

    } break;

    case NodeType_VARIABLE_ASSIGNMENT: {
      if (!node->identifier) {
        throw std::runtime_error("Null Identifier");
      }
      std::string identifier = node->identifier->name;

      if (!node->expression) {
        throw std::runtime_error("Null Expression");
      }
      const ASTNode &expression = *node->expression;
      const std::string writtenExpression = writeExpression(expression);

      myCode.push_back(std::format("{} {} = {};", getBlock(), identifier,
                                   writtenExpression));
    } break;

    case NodeType_FUNCTION_DECLARATION: {
      if (!node->identifier) {
        throw std::runtime_error("Null Identifier");
      }
      std::string identifier = node->identifier->name;

      const EsllType &esllType = node->esllType;
      const std::string cType = typeToCType(esllType);

      const auto &args = node->args;

      std::string codepush = "";
      codepush += std::format("{}{} {}(", getBlock(), cType, identifier);
      for (const auto &arg : args) {
        codepush += std::format("{} {}", typeToCType(arg->esllType),
                                arg->identifier->name);

        if (arg != args.back()) {
          codepush += ", ";
        }
      }

      codepush += ") {";
      myCode.push_back(codepush);
    } break;

    case NodeType_IF: {
      if (!node->expression) {
        throw std::runtime_error("Null Expression");
      }
      const ASTNode &expression = *node->expression;
      const std::string writtenExpression = writeExpression(expression);

      myCode.push_back(getBlock() + "if (" + writtenExpression + ") {");
    } break;

    case NodeType_RETURN: {
      if (!node->expression) {
        throw std::runtime_error("Null Expression");
      }
      const ASTNode &expression = *node->expression;
      const std::string writtenExpression = writeExpression(expression);

      myCode.push_back(getBlock() + "return " + writtenExpression + ";");
    } break;

    case NodeType_ELIF: {
      if (!node->expression) {
        throw std::runtime_error("Null Expression");
      }
      const ASTNode &expression = *node->expression;
      const std::string writtenExpression = writeExpression(expression);

      myCode.push_back(getBlock() + "else if (" + writtenExpression + ") {");
    } break;

    case NodeType_ELSE: {
      myCode.push_back(getBlock() + "else {");
    } break;

    case NodeType_WHILE: {
      if (!node->expression) {
        throw std::runtime_error("Null Expression");
      }
      const ASTNode &expression = *node->expression;
      const std::string writtenExpression = writeExpression(expression);

      myCode.push_back(getBlock() + "while (" + writtenExpression + ") {");
    } break;

    case NodeType_END: {
      if (block == 0) {
        // throw std::runtime_error("Misplaced End");
      }

      myCode.push_back("}");
      block--;
    } break;

    default: {
      myCode.push_back(getBlock() + writeExpression(*node.get()) + ";");
    } break;
    }
  }

  myCode.push_back(R"(
int main() {
  esll_main();
}
  )");

  return myCode;
}
