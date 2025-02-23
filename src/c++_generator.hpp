#include <memory>
#include <string>
#include <vector>

struct ASTNode;

std::vector<std::string>
generate_cpp(const std::vector<std::unique_ptr<ASTNode>> &astNodes);
