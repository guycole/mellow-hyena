#include <iostream>

#include "decoder.h"
#include "decoder_configuration.h"

namespace decoder {

Decoder::Decoder(void) {
    std::cout << "decoder constructor" << std::endl;
    historian = new decoder::Historian();
}

Decoder::~Decoder(void) {
    std::cout << "decoder destructor" << std::endl;
}

int Decoder::converter(std::string raw_buffer) {
    // buffer looks like "*f6d8c9833540611d6ebdee841425;"
    // *8da0c53899080612c8040979d912;
    // test for "*" and ";" 
    std::size_t asterisk_ndx = raw_buffer.find("*");
    if (asterisk_ndx == std::string::npos) {
        std::cout << "not found asterisk" << std::endl;
        return -1;
    }

    std::size_t semicolon_ndx = raw_buffer.find(";");
    if (semicolon_ndx == std::string::npos) {
        std::cout << "not found semicolon" << std::endl;
        return -1;
    }

    // remove the * and ;
    std::string temp_string = raw_buffer.substr(asterisk_ndx + 1, semicolon_ndx - asterisk_ndx - 1);
    //temp_string = "8D4840D6202CC371C32CE0576098"; // aircraft identity
    //temp_string = "8D485020994409940838175B284F"; // airborne velocity sub type 1
    //temp_string = "8DA05F219B06B6AF189400CBC33F"; // airborne velocity sub type 3

    //std::cout << "raw_buffer:" << raw_buffer << std::endl;
    //std::cout << "temp_string:" << temp_string << std::endl;

    long unsigned ii, jj;
    for (ii=0, jj=0; ii < temp_string.length(); ii+=2, jj++) { 
        std::string short_buffer = temp_string.substr(ii, 2);
        converted_array[jj] = std::stoi(short_buffer, nullptr, 16);
    }

    converted_array_size = jj;

    return 0;
}

void Decoder::dispatcher() {
    int download_format = converted_array[0] >> 3;
    //std::cout << download_format << std::endl;

    switch (download_format) {
        case 11:
            std::cout << "downlink format 11" << std::endl;
            break;
        case 17:
            std::cout << "downlink format 17" << std::endl;
//            adsb();
            break;
        case 18:
            std::cout << "downlink format 18" << std::endl;
//            adsb();
            break;
        default:
            std::cout << "downlink format default:" << download_format << std::endl;
            break;
    }
}

int Decoder::string_to_decoder(std::string raw_buffer) {
    int flag = converter(raw_buffer);

    if (flag < 0) {
        std::cout << "converter error noted" << std::endl;
    } else {
        std::cout << "converter success" << std::endl;
        dispatcher();
        historian->record_update("aaa");
    }

    return flag;
}

int Decoder::pipe_to_decoder() {
    std::string raw_buffer;

    std::cout << "pipe_to_decoder" << std::endl;

    while (std::getline(std::cin, raw_buffer)) {
        if (raw_buffer.empty()) {
            break;
        }

        string_to_decoder(raw_buffer);
    }

    return EXIT_SUCCESS;
}

} // namespace decoder