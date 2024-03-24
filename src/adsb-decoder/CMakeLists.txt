# 
cmake_minimum_required(VERSION 3.14)

project(decoder)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall")

set(DECODER_VERSION_MAJOR 0)
set(DECODER_VERSION_MINOR 0)

include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip
)
FetchContent_MakeAvailable(googletest)

configure_file(
    "${PROJECT_SOURCE_DIR}/DecoderConfiguration.h.in"
    "${PROJECT_BINARY_DIR}/decoder_configuration.h"
)

add_executable(decoder decoder.cc driver.cc historian.cc)

target_include_directories(decoder PUBLIC "${PROJECT_BINARY_DIR}")

# message(STATUS "Looking for someheader.h")

# https://google.github.io/googletest/
# https://stackoverflow.com/questions/50861636/using-google-tests-with-cmake-ctest-with-the-new-command-gtest-discover-tests
enable_testing()

add_executable(hello_test hello_test.cc)

add_executable(decoder_test decoder_test.cc)

target_link_libraries(hello_test GTest::gtest_main)

target_link_libraries(decoder_test GTest::gtest_main)

include(GoogleTest)
gtest_discover_tests(decoder_test hello_test)