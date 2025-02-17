from __future__ import annotations

from tokenizer import tokenize
from asttree import ASTNode, generate_ast_tree
from generators.python_generator import generate_python
from generators.c_generator import generate_c

variable_tracker: dict[str, str] = {}


def main() -> None:
    ESLL_FILE = "main.esll"

    # Read from file
    full_text = ""
    with open(ESLL_FILE, "r") as f:
        full_text = f.read()
    lines = full_text.split("\n")

    print(" -- TOKENS -- ")
    tokenized_lines = tokenize(lines)

    for tokenized_line in tokenized_lines:
        print("LINE")
        for token in tokenized_line:
            print(token)


    # CREATE ESL TREE
    print(" -- ESL TREE -- ")
    ast_nodes = generate_ast_tree(tokenized_lines)

    print(" -- CODE GENERATION -- ")
    my_code = generate_c(ast_nodes)

    # Write to file
    with open("mycode.c", "w+") as f:
        for line in my_code:
            f.write(line + "\n")


main()
