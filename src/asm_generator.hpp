#include <memory>
#include <string>
#include <vector>

struct ASTNode;

std::vector<std::string>
generate_asm(const std::vector<std::unique_ptr<ASTNode>> &astNodes);
