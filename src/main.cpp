#include <fstream>
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
  std::vector<std::string> lines;
  {
    std::ifstream esllFile("main.esll");
    for (std::string line; getline(esllFile, line);) {
      lines.push_back(line);
    }
    esllFile.close();
  }

  printf("Tokenizing...\n");
  std::vector<std::vector<Token>> tokenizedLines = tokenize(lines);

  // Print the tokenized lines
  printf("------------------------------------------\n");
  for (int i = 0; i < tokenizedLines.size(); i++) {
    printf("Line %d tokens:\n", i + 1);
    for (int j = 0; j < tokenizedLines[i].size(); j++) {
      printf("  Type: %d, Value: %s\n", tokenizedLines[i][j].tokenType,
             tokenizedLines[i][j].value.c_str());
    }
  }

  printf("Generating Abstract Syntax Tree...\n");
  auto astNodes = generateASTTree(tokenizedLines);
  for (const auto &node : astNodes) {
    node->print();
    std::cout << "\n";
  }

  printf("Generating C++ Output...\n");
  std::vector<std::string> myCode = generate_cpp(astNodes);
  {
    std::ofstream outputFile("build/main.cpp");
    for (std::string line : myCode) {
      outputFile << line << "\n";
    }
    outputFile.close();
  }

  return 0;
}
