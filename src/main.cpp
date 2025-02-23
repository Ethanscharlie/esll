#include <iostream>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <string>
#include <vector>

#include "asttree.hpp"
#include "c++_generator.hpp"
#include "tokenizer.hpp"

int main() {
  printf("Reading from file...\n");
  std::vector<std::string> lines = {

      "Decimal SCREEN_WIDTH 800",
      "Decimal SCREEN_HEIGHT 800",
      "Decimal SPEED 10",
      "Decimal GRAVITY 0.35",
      "Decimal JUMP_POWER 70",
      "Decimal boxX 100",
      "Decimal boxY 100",
      "Decimal boxW 100",
      "Decimal boxH 100",
      "Decimal boxVelocityY 0",
      "Void start()",
      "end",
      "Void draw()",
      "  setBackground(100, 200, 100)",
      "  boxVelocityY boxVelocityY + GRAVITY * deltatime",
      "  if pressingKey(\">\")",
      "    boxX boxX + SPEED * deltatime",
      "  end",
      "  if pressingKey(\"<\")",
      "    boxX boxX - SPEED * deltatime",
      "  end",
      "  if pressingKey(\" \")",
      "    boxVelocityY -JUMP_POWER * deltatime",
      "  end",
      "  boxY boxY + boxVelocityY * deltatime",
      "  if boxY + boxH > SCREEN_HEIGHT",
      "    boxY SCREEN_HEIGHT - boxH",
      "    boxVelocityY 0",
      "  end",
      "  fill(255, 0, 0)",
      "  drawRectangle(boxX, boxY, boxW, boxH)",
      "end",
  };

  printf("Tokenizing...\n");
  std::vector<std::vector<Token>> tokenizedLines = tokenize(lines);

  // Print the tokenized lines
  // printf("------------------------------------------\n");
  // for (int i = 0; i < tokenizedLines.size(); i++) {
  //   printf("Line %d tokens:\n", i + 1);
  //   for (int j = 0; j < tokenizedLines[i].size(); j++) {
  //     printf("  Type: %d, Value: %s\n", tokenizedLines[i][j].tokenType,
  //            tokenizedLines[i][j].value.c_str());
  //   }
  // }

  printf("Generating Abstract Syntax Tree...\n");
  auto astNodes = generateASTTree(tokenizedLines);
  for (const auto &node : astNodes) {
    if (!node->identifier) {
      continue;
    }
    printf("%s\n", node->identifier->name.c_str());
  }

  printf("Generating C++ Output...\n");
  std::vector<std::string> myCode = generate_cpp(astNodes);
  printf("------------------------------------------\n");
  for (std::string line : myCode) {
    printf("%s\n", line.c_str());
  }

  return 0;
}
