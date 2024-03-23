#include <iostream>

#include "decoder.h"

int main(int argc, char* argv[]) {
    const std::string banner = "decoder 0.0"; //TODO get version from cmake

    std::cout << "begin" << std::endl;
    std::cout << banner << std::endl;
    std::cout << __DATE__ << " " << __TIME__ << std::endl;

    std::cout << "end" << std::endl;

    int ret_value = EXIT_SUCCESS;

    return ret_value;
};