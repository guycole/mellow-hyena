
#include <stdlib.h>
#include <string.h>

#include "utility.h"

int type_code_1_4(SAMPLE_PTR sample) {
    // flight identifier
    char cc;
    char id_buffer[MAX_IDENTIFICATION_LENGTH];
    strlcpy(id_buffer, "        \0", MAX_IDENTIFICATION_LENGTH);

    unsigned long ltemp = sample->me;

    for (size_t ii=0, jj=7; ii < 8; ii++, jj--) {
        cc = (char) (ltemp & 0x3f);
        if (cc < 0x20) {
            cc = cc | 0x40; // convert to ASCII
        }
        id_buffer[jj] = cc;
        ltemp = ltemp >> 6;
    }

    strlcpy(sample->identification, id_buffer, MAX_IDENTIFICATION_LENGTH);
    sample->wake_vertex = (unsigned short) (ltemp & 0x3);

    return EXIT_SUCCESS;
}

int type_code_9_18_20_22(SAMPLE_PTR sample) {
    // position

    unsigned long ltemp = sample->me;
    unsigned int lon_cpr = (unsigned int) (ltemp & 0x1ffff);
    ltemp = ltemp >> 17;
    unsigned int lat_cpr = (unsigned int) (ltemp & 0x1ffff);
    ltemp = ltemp >> 17;
    unsigned short cpr_format_flag = (unsigned short) (ltemp & 0x1);
    ltemp = ltemp >> 1;
    unsigned short time_flag = (unsigned short) (ltemp & 0x1);
    ltemp = ltemp >> 1;
    unsigned short encoded_altitude = (unsigned short) (ltemp & 0xfff);
    ltemp = ltemp >> 12;
    unsigned short single_antenna_flag = (unsigned short) (ltemp & 0x1);
    ltemp = ltemp >> 1;
    unsigned short surveillance_status = (unsigned short) (ltemp & 0x3);

    return EXIT_SUCCESS;
}