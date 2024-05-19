#include <stdio.h>

#include "decoder.h"

#define MAX_BUFFER 64

int main(int argc, char *argv[]) {
    char buffer[MAX_BUFFER];

    snprintf(buffer, MAX_BUFFER, "decoder %d.%d compiled on %s at %s", DECODER_VERSION_MAJOR, DECODER_VERSION_MINOR, __DATE__, __TIME__);

    printf("%s\n", buffer);

    string_to_decoder("*8D4840D6202CC371C32CE0576098;");
}