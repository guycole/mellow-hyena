#include <iostream>

#include "decoder.h"
#include "historian.h"

namespace decoder {

Historian::Historian(void) {
    std::cout << "historian constructor" << std::endl;
}

Historian::~Historian(void) {
    std::cout << "historian destructor" << std::endl;
}

void Historian::record_update(std::string adsb_hex) {
    std::cout << "historian record_update" << std::endl;
}

} // namespace decoder