#ifndef HYENA_SAMPLE_H
#define HYENA_SAMPLE_H

#define RAW_SAMPLE_EMPTY -202
#define RAW_SAMPLE_NULL -203
#define RAW_SAMPLE_MISSING_SEMICOLON -204
#define RAW_SAMPLE_MISSING_ASTERISK -205

#define MAX_CONVERTED_SAMPLE_LENGTH 32
#define MAX_RAW_SAMPLE_LENGTH 64
#define MAX_IDENTIFICATION_LENGTH 16

typedef struct {
    char raw_sample[MAX_RAW_SAMPLE_LENGTH];
    size_t converted_sample_size;
    unsigned char converted_sample[MAX_CONVERTED_SAMPLE_LENGTH];
    unsigned short ca;    // transponder capability
    unsigned short df;    // downlink format
    unsigned int icao;    // icao address
    unsigned long me;     // message, extended squitter
    unsigned short me_tc; // message type code
    unsigned int pi;      // parity/interrogator ID
    unsigned short wake_vertex;
    char identification[MAX_IDENTIFICATION_LENGTH];

} SAMPLE, *SAMPLE_PTR;

extern int sample_converter(SAMPLE_PTR sample);
extern int sample_df_17_18_parser(SAMPLE_PTR sample);
extern void sample_dumper(SAMPLE_PTR sample);

#endif
