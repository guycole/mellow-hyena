#include <stdio.h>
#include <stdlib.h>

#include "decoder.h"

#define MAX_BUFFER 64

int main(int argc, char *argv[]) {
    char buffer[MAX_BUFFER];

    snprintf(buffer, MAX_BUFFER, "decoder %d.%d compiled on %s at %s", DECODER_VERSION_MAJOR, DECODER_VERSION_MINOR, __DATE__, __TIME__);
    printf("%s\n", buffer);

    string_to_decoder("*8D4840D6202CC371C32CE0576098;");
    string_to_decoder("*8D40621D58C382D690C8AC2863A7;");
    string_to_decoder("*8D40621D58C386435CC412692AD6;");
 
    return EXIT_SUCCESS;
}