#include <gtest/gtest.h>

#include "decoder.h"

namespace {

TEST(DecoderTest, MalformedStringTest) {
    decoder::Decoder *decoder = new decoder::Decoder();

    int flag = decoder->string_to_decoder("*8D4840D6202CC371C32CE0576098;");
    EXPECT_EQ(0, flag); 

    flag = decoder->string_to_decoder("8D4840D6202CC371C32CE0576098;");
    EXPECT_EQ(-1, flag);

    flag = decoder->string_to_decoder("*8D4840D6202CC371C32CE0576098");
    EXPECT_EQ(-1, flag); 
}

}  // namespace