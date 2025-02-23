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
      expression += ", ";
    }
    expression += ")";
  } break;
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

    const auto &args = node.args;
    expression += identifier;
    expression += "(";
    for (const auto &arg : args) {
      expression += writeExpression(*arg.get());
      expression += ", ";
    }
    expression += ")";
  } break;

  case NodeType_ADD: {
    expression += checkNode(node.first.get());
    expression += "+";
    expression += checkNode(node.second.get());
  } break;
  }

  return expression;
}

std::vector<std::string>
generate_cpp(const std::vector<std::unique_ptr<ASTNode>> &astNodes) {
  std::vector<std::string> myCode;
  std::vector<std::string> myCodeTemp;
  myCodeTemp.push_back(R"(
// Includes
#include "stdio.h"
#include <stdlib.h>
#include <SDL3/SDL.h>

// Global variables
float esll_deltatime = 0;
float esllbackend_lastTime = 0;

// Functions
void esll_print(const char* text) {
    printf(text);
    printf("\\n");
}

// Graphics
SDL_Window *window;
SDL_Renderer *renderer;

void esllbackend_makeWindow(int width, int height) {
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        printf("SDL_Init Error: %s\\n", SDL_GetError());
    }

    if (!SDL_CreateWindowAndRenderer("ESLL Window", width, height, SDL_WINDOW_RESIZABLE, &window, &renderer)) {
        printf("Couldn't create window and renderer: %s\\n", SDL_GetError());
    }
}

void esllbackend_draw() {
    // Deltatime
    Uint64 currentTime = SDL_GetPerformanceCounter();
    float inbetweenTime = currentTime - esllbackend_lastTime;
    esll_deltatime = inbetweenTime * 1000 / SDL_GetPerformanceFrequency() * 0.1;
    esllbackend_lastTime = SDL_GetPerformanceCounter();

    SDL_Event event;
    SDL_PollEvent(&event);
    if (event.type == SDL_EVENT_QUIT) {
        exit(0);
    }

    SDL_RenderPresent(renderer);
}

// Interactable graphics
void esll_setBackground(int r, int g, int b) {
    SDL_SetRenderDrawColor(renderer, r, g, b, 255);
    SDL_RenderClear(renderer);
}

void esll_fill(int r, int g, int b) {
    SDL_SetRenderDrawColor(renderer, r, g, b, 255);
}

void esll_drawRectangle(float x, float y, float w, float h) {
    SDL_FRect rect = { x, y, w, h };
    SDL_RenderFillRect(renderer, &rect);
}

bool esll_pressingKey(char* key) {
    const bool *keyState = SDL_GetKeyboardState(NULL);

    if (key == " ") {
        return keyState[SDL_SCANCODE_SPACE];
    } else if (key == ">") {
        return keyState[SDL_SCANCODE_RIGHT];
    } else if (key == "<") {
        return keyState[SDL_SCANCODE_LEFT];
    } else if (key == "^") {
        return keyState[SDL_SCANCODE_UP];
    } else if (key == "v") {
        return keyState[SDL_SCANCODE_DOWN];
    }

    return false;
}
      )");

  int block = 0;
  for (int lineNumber = 0; lineNumber < astNodes.size(); lineNumber ++) {
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
    } break;
    }
  }

  return myCode;
}
