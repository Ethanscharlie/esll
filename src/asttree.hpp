#include "tokenizer.hpp"
#include <memory>
#include <vector>

typedef enum NodeType {
  NodeType_NONE,
  NodeType_IDENTIFIER,
  NodeType_LITERAL,
  NodeType_TYPE,

  NodeType_ADD,
  NodeType_SUBTRACT,
  NodeType_MULTIPLY,
  NodeType_DIVIDE,
  NodeType_MODULUS,

  NodeType_EQUALS,
  NodeType_GREATER_THAN,
  NodeType_LESS_THAN,
  NodeType_AND,
  NodeType_OR,

  NodeType_VARIABLE_DECLARATION,
  NodeType_FUNCTION_DECLARATION,
  NodeType_VARIABLE_ASSIGNMENT,
  NodeType_FUNCTION_CALL,

  NodeType_FUNCTION_ARGUMENT_DECLARATION,

  NodeType_IF,
  NodeType_WHILE,
  NodeType_END,
  NodeType_ELIF,
  NodeType_ELSE,
  NodeType_RETURN
} NodeType;

typedef enum EsllType {
  EsllType_VOID,
  EsllType_INTEGER,
  EsllType_DECIMAL,
  EsllType_BOOLEAN,
  EsllType_STRING
} EsllType;

struct ASTNode {
  ASTNode(NodeType nodeType, std::string value)
      : nodeType(nodeType), value(value) {}
  ASTNode(NodeType nodeType) : nodeType(nodeType), value("") {}
  NodeType nodeType;
  std::string value;
  std::string name;
  std::unique_ptr<ASTNode> first;
  std::unique_ptr<ASTNode> second;
  std::unique_ptr<ASTNode> identifier;
  std::unique_ptr<ASTNode> expression;
  EsllType esllType;
  std::vector<std::unique_ptr<ASTNode>> args;
};

std::vector<std::unique_ptr<ASTNode>>
generateASTTree(std::vector<std::vector<Token>> tokenizedLines);
