#include <filesystem>
#include <fstream>
#include <iostream>
#include <signal.h>
#include <stdbool.h>
#include <stdexcept>
#include <stdio.h>
#include <stdlib.h>
#include <streambuf>
#include <string.h>
#include <string>
#include <vector>

#include "asttree.hpp"
#include "c++_generator.hpp"
#include "tokenizer.hpp"

int main(int argc, char *argv[]) {
  printf("Reading from file...\n");
  std::vector<std::string> lines;
  {
    std::ifstream esllFile(argv[1]);

    if (!esllFile) {
      throw std::runtime_error("File not found");
    }

    for (std::string line; getline(esllFile, line);) {
      lines.push_back(line);
    }
    esllFile.close();
  }

  printf("Tokenizing...\n");
  std::vector<std::vector<Token>> tokenizedLines = tokenize(lines);

  // Print the tokenized lines
  printf("------------------------------------------\n");
  // for (int i = 0; i < tokenizedLines.size(); i++) {
  //   printf("Line %d tokens:\n", i + 1);
  //   for (int j = 0; j < tokenizedLines[i].size(); j++) {
  //     printf("  Type: %d, Value: %s\n", tokenizedLines[i][j].tokenType,
  //            tokenizedLines[i][j].value.c_str());
  //   }
  // }

  printf("Generating Abstract Syntax Tree...\n");
  auto astNodes = generateASTTree(tokenizedLines);
  // for (const auto &node : astNodes) {
  //   node->print();
  //   std::cout << "\n";
  // }

  printf("Generating C++ Output...\n");
  std::vector<std::string> myCode = generate_cpp(astNodes);

  printf("Creating build folder...\n");

  std::filesystem::create_directory("build");

  std::ofstream outputFile("build/main.cpp");
  for (std::string line : myCode) {
    outputFile << line << "\n";
  }
  outputFile.close();

  system("g++ build/main.cpp -o build/main");

  return 0;
}
