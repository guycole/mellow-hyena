#ifndef HYENA_DF_17_18_H_ 
#define HYENA_DF_17_18_H_

#include "historian.h"

namespace decoder {

class DF_17_18 {
public:
    DF_17_18(void);
    ~DF_17_18(void);

    int df_17_18_parser(OBSERVATION_PTR observation);
};

} // namespace decoder

#endif // HYENA_DF_17_18_H_