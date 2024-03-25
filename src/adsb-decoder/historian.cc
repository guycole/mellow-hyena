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

void Historian::reset(OBSERVATION_PTR observation) {
    std::cout << "historian reset" << std::endl;

    observation->adsb_hex = 0;
    observation->df = 0;
}
  
void Historian::update(OBSERVATION_PTR observation) {
    std::cout << "historian update" << std::endl;

    std::cout << archive.size() << std::endl;

    // https://leimao.github.io/blog/CPP-HashMaps/
    archive.insert({observation->adsb_hex, *observation});

    std::cout << archive.size() << std::endl;
}

} // namespace decoder