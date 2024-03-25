#include <iostream>

#include "df_17_18.h"

namespace decoder {

DF_17_18::DF_17_18(void) {
    std::cout << "df_17_18 constructor" << std::endl;
}

DF_17_18::~DF_17_18(void) {
    std::cout << "df_17_18 destructor" << std::endl;
}

int DF_17_18::df_17_18_parser(OBSERVATION_PTR observation) {
    std::cout << "parser" << std::endl;
    return 0;
}


} // namespace decoder