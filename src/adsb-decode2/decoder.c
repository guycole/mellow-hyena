#include <stdio.h>
#include <string.h>

#include "decoder.h"

#define MAX_BUFFER 64

int converter(const char* raw_buffer) {
    char work_buffer[MAX_BUFFER];

    //TODO test raw_buffer for null and empty

    // buffer looks like "*f6d8c9833540611d6ebdee841425;"
    // test for "*" and ";" 
    char *cndx1 = strchr(raw_buffer, '*');
    if (cndx1 == (char *) NULL) {
        fprintf(stderr, "not found asterisk\n");
        return RAW_BUFFER_MISSING_ASTERISK;
    }

    char *cndx2 = strchr(raw_buffer, ';');
    if (cndx2 == (char *) NULL) {
        fprintf(stderr, "not found semicolon\n");
        return RAW_BUFFER_MISSING_SEMICOLON;
    }

    // remove the * and ;
    strcpy(work_buffer, cndx1+1);
    work_buffer[cndx2-cndx1-1] = '\0';
    
    printf("win\n");
    printf("%s\n", work_buffer);

//    *cndx2 = '\0';
//    printf("%s\n", cndx1+1);

// if ((cndx1 = strchr(key, '.')) != (char *) NULL) {




    return 0;
}

int string_to_decoder(const char* buffer) {
    int retflag = converter(buffer);
    return retflag;
}