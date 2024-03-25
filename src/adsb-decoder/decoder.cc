#include <iostream>

#include <glog/logging.h>

#include "decoder.h"
#include "df_17_18.h"

namespace decoder {

Decoder::Decoder(void) {
    std::cout << "decoder constructor" << std::endl;
    historian = new decoder::Historian();

    // TODO replace initialization with gflags
    google::InitGoogleLogging("INFO");
    FLAGS_logtostderr= 1;
    LOG(INFO) << "Found cookies";
}

Decoder::~Decoder(void) {
    std::cout << "decoder destructor" << std::endl;
}

int Decoder::converter(std::string raw_buffer) {
    // buffer looks like "*f6d8c9833540611d6ebdee841425;"
    // test for "*" and ";" 
    std::size_t asterisk_ndx = raw_buffer.find("*");
    if (asterisk_ndx == std::string::npos) {
        LOG(INFO) << "not found asterisk";
        return -1;
    }

    std::size_t semicolon_ndx = raw_buffer.find(";");
    if (semicolon_ndx == std::string::npos) {
        LOG(INFO) << "not found semicolon";
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

int Decoder::dispatcher() {
    int retflag = 0;
    int download_format = converted_array[0] >> 3;
    LOG(INFO) << "download_format:" << download_format;

    if (download_format == 11) {
        std::cout << "downlink format 11" << std::endl;
    } else if ((download_format == 17) || (download_format == 18)) {
        DF_17_18* parser = new DF_17_18();
        retflag = parser->df_17_18_parser(&observation);
        free(parser);
    } else {
        std::cout << "downlink format default:" << download_format << std::endl;
    }

    return retflag;
}

int Decoder::string_to_decoder(std::string raw_buffer) {
    int retflag = converter(raw_buffer);

    if (retflag < 0) {
        std::cout << "converter error noted" << std::endl;
    } else {
        std::cout << "converter success" << std::endl;
        historian->reset(&observation);
        retflag = dispatcher();
        if (retflag == 0) {
            historian->update(&observation);
        }
    }

    return retflag;
}

int Decoder::pipe_to_decoder() {
    int retflag;
    int failure = 0, success = 0;
    std::string raw_buffer;

    std::cout << "pipe_to_decoder" << std::endl;

    while (std::getline(std::cin, raw_buffer)) {
        if (raw_buffer.empty()) {
            break;
        }

        retflag = string_to_decoder(raw_buffer);
        if (retflag < 0) {
            failure++;
        } else {
            success++;
        }
    }

    return EXIT_SUCCESS;
}

} // namespace decoder