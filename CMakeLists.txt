cmake_minimum_required(VERSION 3.0)
set (CMAKE_CXX_STANDARD 20)
project(esll)

add_executable(esll 
  src/main.cpp
  src/asttree.cpp
  src/tokenizer.cpp
  src/c++_generator.cpp
)
