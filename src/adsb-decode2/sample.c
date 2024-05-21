#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "sample.h"
#include "utility.h"

int sample_converter(SAMPLE_PTR sample) {
    if (sample->raw_sample == (char *) NULL) {
        fprintf(stderr, "null raw sample\n");
        return RAW_SAMPLE_NULL;
    }

    if (strlen(sample->raw_sample) == 0) {
        fprintf(stderr, "empty raw sample\n");
        return RAW_SAMPLE_EMPTY;
    }

    // buffer looks like "*f6d8c9833540611d6ebdee841425;"
    // test for "*" and ";" 
    char *cndx1 = strchr(sample->raw_sample, '*');
    if (cndx1 == (char *) NULL) {
        fprintf(stderr, "not found asterisk\n");
        return RAW_SAMPLE_MISSING_ASTERISK;
    }

    char *cndx2 = strchr(sample->raw_sample, ';');
    if (cndx2 == (char *) NULL) {
        fprintf(stderr, "not found semicolon\n");
        return RAW_SAMPLE_MISSING_SEMICOLON;
    }

    // remove the * and ;
    char temp_buffer[MAX_RAW_SAMPLE_LENGTH];
    strcpy(temp_buffer, cndx1+1);
    temp_buffer[cndx2-cndx1-1] = '\0';

    // ASCII conversion
    size_t ii, jj; 
    char short_buffer[3];
    for (ii=0, jj=0; ii < strlen(temp_buffer); ii+=2, jj++) {
        strncpy(short_buffer, temp_buffer+ii, 2); 
        short_buffer[2] = '\0';
        //printf("%s\n", short_buffer);
        sample->converted_sample[jj] = (unsigned char)strtol(short_buffer, NULL, 16);
    }

    sample->converted_sample_size = jj;

    sample->ca = sample->converted_sample[0] & 0x07; 
    sample->df = sample->converted_sample[0] >> 3;

    sample->icao = 0;
    for (ii=1; ii < 4; ii++) {
        sample->icao = (sample->icao << 8) | sample->converted_sample[ii];
    }

    sample->me = 0;
    for (ii=4; ii < 11; ii++) {
        sample->me = (sample->me << 8) | sample->converted_sample[ii];
    }

    sample->me_tc = (unsigned short) (sample->me >> 51);

    sample->pi = 0;
    for (ii=11; ii < 14; ii++) {
        sample->pi = (sample->pi << 8) | sample->converted_sample[ii];
    }
  
    return EXIT_SUCCESS;
}

int sample_df_17_18_parser(SAMPLE_PTR sample) {
    printf("df 17_18\n");

    switch (sample->me_tc) {
        case 1 ... 4: // identification and wake vortex category
            type_code_1_4(sample);
            break;
        case 9 ... 18: // airborne position
            type_code_9_18_20_22(sample); 
            break;
        case 20 ... 22: // airborne position
            type_code_9_18_20_22(sample); 
            break;
        default:
            printf("unknown me_tc\n");
    }

    return EXIT_SUCCESS;    
}

void sample_dumper(SAMPLE_PTR sample) {
    printf("-x-x-x- dumper -x-x-x-\n");

    printf("raw_sample: %s\n", sample->raw_sample);
    
    printf("converted_sample_size: %ld\n", sample->converted_sample_size);
    printf("converted_sample: ");
    for (size_t ii=0; ii < sample->converted_sample_size; ii++) {
        printf("%02x", sample->converted_sample[ii]);
    }
    printf("\n");

    printf("ca: %d\n", sample->ca);
    printf("df: %d\n", sample->df);
    printf("icao: %x\n", sample->icao);
    printf("me: %lx\n", sample->me);
    printf("me_tc: %d\n", sample->me_tc);
    printf("pi: %x\n", sample->pi);

    printf("wake vortex: %x\n", sample->wake_vertex);
    printf("identification: %s\n", sample->identification);

    printf("-x-x-x- dumper -x-x-x-\n");
}
