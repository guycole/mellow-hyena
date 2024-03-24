#include <gtest/gtest.h>

#include "decoder.h"

namespace {

TEST(DecoderTest, ParserSuccess) {
    decoder::Decoder *decoder = new decoder::Decoder();
    //decoder->string_to_decoder("*f6d8c9833540611d6ebdee841425;");

  // Expect two strings not to be equal.
  EXPECT_STRNE("hello", "world");
  // Expect equality.
  EXPECT_EQ(7 * 6, 42);
}

}  // namespace