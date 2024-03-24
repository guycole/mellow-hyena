#ifndef HYENA_HISTORIAN_H_ 
#define HYENA_HISTORIAN_H_

namespace decoder {

class Historian {
public:
    Historian(void);
    ~Historian(void);

    void record_update(std::string adsb_hex);
};

} // namespace decoder

#endif // HYENA_HISTORIAN_H_