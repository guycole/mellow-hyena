#include <ctime>

class row {
private:
    std::string adsb_hex;
    std::time_t first_observed;
    std::time_t last_observed;
};

class historian {
public:
    void add_entry(void);
private:
    int xx;
};
