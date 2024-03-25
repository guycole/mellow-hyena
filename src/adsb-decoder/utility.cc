#include <iostream>

#include "utility.h"

namespace decoder {

Utility::Utility(void) {
    std::cout << "utility constructor" << std::endl;
}

Utility::~Utility(void) {
    std::cout << "utility destructor" << std::endl;
}

} // namespace decoder