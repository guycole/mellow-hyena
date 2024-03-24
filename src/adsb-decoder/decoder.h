#ifndef HYENA_DECODER_H_ 
#define HYENA_DECODER_H_

#include <string>

#include "historian.h"

#define CONVERTED_ARRAY_LIMIT 14

namespace decoder {

class Decoder {
public:
    Decoder(void);
    ~Decoder(void);

    int pipe_to_decoder();
    int string_to_decoder(std::string raw_buffer);
private:
    int converter(std::string raw_buffer);
    void dispatcher();

    int converted_array_size;
    unsigned short int converted_array[CONVERTED_ARRAY_LIMIT];

    decoder::Historian *historian;
};

} // namespace decoder

#endif // HYENA_DECODER_H_