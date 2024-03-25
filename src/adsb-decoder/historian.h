#ifndef HYENA_HISTORIAN_H_ 
#define HYENA_HISTORIAN_H_

#include <unordered_map>
#include <string>
#include <iostream>

namespace decoder {

typedef struct {
    unsigned int adsb_hex;          // icao address
    unsigned int observation_count; // observation population
    unsigned short df;              // downlink format
    std::time_t first_observed;     // utc timestamp
    std::time_t last_observed;      // utc_timestamp
} OBSERVATION, *OBSERVATION_PTR;

class Historian {
public:
    Historian(void);
    ~Historian(void);

    void reset(OBSERVATION_PTR observation);
    void update(OBSERVATION_PTR observation);
private:
    std::unordered_map<int, OBSERVATION> archive;
};

} // namespace decoder

#endif // HYENA_HISTORIAN_H_