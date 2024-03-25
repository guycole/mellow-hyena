#include <iostream>

#include "decoder.h"
#include "decoder_configuration.h"

#define MAX_BANNER 64

// TODO https://github.com/gflags/gflags

int main(int argc, char *argv[]) {
	char banner [MAX_BANNER];

	snprintf(banner, MAX_BANNER, "decoder %d.%d compiled at %s on %s", DECODER_VERSION_MAJOR, DECODER_VERSION_MINOR, __TIME__, __DATE__);

    std::cout << "begin" << std::endl;
    std::cout << banner << std::endl;

    decoder::Decoder *decoder = new decoder::Decoder();
	decoder->pipe_to_decoder();

    std::cout << "end" << std::endl;

	int ret_value = EXIT_SUCCESS;

	return ret_value;
}