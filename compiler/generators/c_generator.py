from asttree import ASTNode, EsllType


def type_to_c_type(esllType: EsllType) -> str:
    if esllType == EsllType.STRING: return "char*"
    elif esllType == EsllType.INTEGER: return "int"
    elif esllType == EsllType.DECIMAL: return "float"
    elif esllType == EsllType.VOID: return "void"
    elif esllType == EsllType.BOOLEAN: return "bool"
    return "TYPENOTFOUND"

def generate_c(ast_nodes: list[ASTNode]) -> list[str]:
    my_code: list[str] = []

    my_code.append(
"""
// Includes
#include "stdio.h"
#include <SDL3/SDL.h>
#include <cstdlib>

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
    SDL_Event event;
    SDL_PollEvent(&event);
    if (event.type == SDL_EVENT_QUIT) {
        exit(0);
    }

    SDL_RenderPresent(renderer);
}

void esll_setBackground(int r, int g, int b) {
    SDL_SetRenderDrawColor(renderer, r, g, b, 255);
    SDL_RenderClear(renderer);
}

""")

    # PYTHON CODE GENERATION
    block = 0
    for node in ast_nodes:

        def get_block() -> str:
            return "    " * block

        def write_expression(node: ASTNode) -> str:
            def checkNode(testing_node: ASTNode | None):
                if testing_node == None:
                    raise SyntaxError("Node was null")

                expression = ""

                if testing_node.nodeType == ASTNode.NodeType.LITERAL:
                    expression += testing_node.value
                    print(f"Literal value: {testing_node.value}")
                elif testing_node.nodeType == ASTNode.NodeType.IDENTIFIER:
                    expression += testing_node.name

                elif node.nodeType == node.NodeType.FUNCTION_CALL:
                    if node.identifier == None:
                        raise SyntaxError("Null Identifier")

                    identifier = node.identifier.name
                    args = node.args
                    expression += f"{identifier}({', '.join([write_expression(arg) for arg in args])})"

                else:
                    print(testing_node.nodeType)
                    expression += write_expression(testing_node)

                return expression

            expression = ""
            if node.nodeType == ASTNode.NodeType.LITERAL:
                expression += node.value
            elif node.nodeType == ASTNode.NodeType.IDENTIFIER:
                expression += node.name

            elif node.nodeType == node.NodeType.FUNCTION_CALL:
                if node.identifier == None:
                    raise SyntaxError("Null Identifier")

                identifier = node.identifier.name
                args = node.args
                expression += f"{identifier}({', '.join([write_expression(arg) for arg in args])})"

            if node.nodeType == ASTNode.NodeType.ADD:
                expression += checkNode(node.first)
                expression += "+"
                expression += checkNode(node.second)

            elif node.nodeType == ASTNode.NodeType.SUBTRACT:
                expression += checkNode(node.first)
                expression += "-"
                expression += checkNode(node.second)

            elif node.nodeType == ASTNode.NodeType.MULTIPLY:
                expression += checkNode(node.first)
                expression += "*"
                expression += checkNode(node.second)

            elif node.nodeType == ASTNode.NodeType.DIVIDE:
                expression += checkNode(node.first)
                expression += "/"
                expression += checkNode(node.second)

            elif node.nodeType == ASTNode.NodeType.MODULUS:
                expression += checkNode(node.first)
                expression += "%"
                expression += checkNode(node.second)

            elif node.nodeType == ASTNode.NodeType.EQUALS:
                expression += checkNode(node.first)
                expression += "=="
                expression += checkNode(node.second)

            elif node.nodeType == ASTNode.NodeType.GREATER_THAN:
                expression += checkNode(node.first)
                expression += ">"
                expression += checkNode(node.second)

            elif node.nodeType == ASTNode.NodeType.LESS_THAN:
                expression += checkNode(node.first)
                expression += "<"
                expression += checkNode(node.second)

            elif node.nodeType == ASTNode.NodeType.AND:
                expression += checkNode(node.first)
                expression += " && "
                expression += checkNode(node.second)

            elif node.nodeType == ASTNode.NodeType.OR:
                expression += checkNode(node.first)
                expression += " || "
                expression += checkNode(node.second)

            return expression

        if node.nodeType == node.NodeType.VARIABLE_DECLARATION:
            if node.identifier == None:
                raise SyntaxError("Null Identifier")
            identifier = node.identifier.name

            if node.esllType == None:
                raise SyntaxError("Null Type")
            esllType = node.esllType
            cType = type_to_c_type(esllType);

            if node.expression == None:
                raise SyntaxError("Null Expression")
            expression = node.expression

            my_code.append(
                f"{get_block()}{cType} {identifier} = {write_expression(expression)};"
            )

        elif node.nodeType == node.NodeType.VARIABLE_ASSIGNMENT:
            if node.identifier == None:
                raise SyntaxError("Null Identifier")

            identifier = node.identifier.name

            if node.expression == None:
                raise SyntaxError("Null Expression")
            expression = node.expression

            my_code.append(
                f"{get_block()}{identifier} = {write_expression(expression)};"
            )

        elif node.nodeType == node.NodeType.FUNCTION_DECLARATION:
            if node.identifier == None:
                raise SyntaxError("Null Identifier")

            if node.esllType == None:
                raise SyntaxError("Null Type")
            esllType = node.esllType
            cType = type_to_c_type(esllType);

            identifier = node.identifier.name
            args = node.args
            my_code.append(
                f"{get_block()}{cType} {identifier}({', '.join([f'{type_to_c_type(arg.esllType)} {arg.identifier.name}' for arg in args])})"
            )
            my_code.append(get_block() + "{")
            block += 1

        elif node.nodeType == node.NodeType.IF:
            if node.expression == None:
                raise SyntaxError("Null Expression")

            expression = node.expression
            my_code.append(f"{get_block()}if ({write_expression(expression)})")
            my_code.append(get_block() + "{")
            block += 1

        elif node.nodeType == node.NodeType.RETURN:
            if node.expression == None:
                raise SyntaxError("Null Expression on return")

            expression = node.expression
            my_code.append(f"{get_block()}return {write_expression(expression)};")

        elif node.nodeType == node.NodeType.ELIF:
            if node.expression == None:
                raise SyntaxError("Null Expression")

            expression = node.expression
            block -= 1
            my_code.append(get_block() + "}")
            my_code.append(f"{get_block()}else if ({write_expression(expression)})")
            my_code.append(get_block() + "{")
            block += 1

        elif node.nodeType == node.NodeType.ELIF:
            block -= 1
            my_code.append(get_block() + "}")
            my_code.append(f"{get_block()}else")
            my_code.append(get_block() + "{")
            block += 1

        elif node.nodeType == node.NodeType.WHILE:
            if node.expression == None:
                raise SyntaxError("Null Expression")

            expression = node.expression
            my_code.append(f"{get_block()}while ({write_expression(expression)})")
            my_code.append(get_block() + "{")
            block += 1

        elif node.nodeType == node.NodeType.END:
            if block == 0:
                raise SyntaxError("Misplaced End")
            my_code.append("}")
            block -= 1

        else:
            my_code.append(f"{get_block()}{write_expression(node)};")

    my_code.append(
"""
int main() {
    esllbackend_makeWindow(800, 800);
    esll_start();

    while (true) {
        esll_draw();
        esllbackend_draw();
    }
}
""")

    return my_code
