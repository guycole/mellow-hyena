#ifndef HYENA_DECODER_H
#define HYENA_DECODER_H

#define DECODER_VERSION_MAJOR 0
#define DECODER_VERSION_MINOR 0

#define RAW_BUFFER_MISSING_SEMICOLON -101
#define RAW_BUFFER_MISSING_ASTERISK -102

typedef struct {
    unsigned int adsb_hex;          // icao address
    unsigned int observation_count; // observation population
    unsigned short df;              // downlink format
    //std::time_t first_observed;     // utc timestamp
    //std::time_t last_observed;      // utc_timestamp
} OBSERVATION, *OBSERVATION_PTR;

extern int string_to_decoder(const char* buffer);

#endif
