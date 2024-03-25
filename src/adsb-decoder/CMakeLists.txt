# 
cmake_minimum_required(VERSION 3.16)

project(decoder)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall")

set(DECODER_VERSION_MAJOR 0)
set(DECODER_VERSION_MINOR 0)

configure_file(
    "${PROJECT_SOURCE_DIR}/DecoderConfiguration.h.in"
    "${PROJECT_BINARY_DIR}/decoder_configuration.h"
)

include_directories("/usr/local/include")

add_executable(decoder decoder.cc df_17_18.cc driver.cc historian.cc utility.cc)

target_include_directories(decoder PUBLIC "${PROJECT_BINARY_DIR}")

# glog
find_package (glog 0.6.0 REQUIRED)
target_link_libraries (decoder glog::glog)

# googletest
message(STATUS "GoogleTest")

include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip
)
FetchContent_MakeAvailable(googletest)

# https://google.github.io/googletest/
# https://stackoverflow.com/questions/50861636/using-google-tests-with-cmake-ctest-with-the-new-command-gtest-discover-tests
enable_testing()

add_executable(hello_test hello_test.cc)

add_executable(decoder_test decoder_test.cc decoder.cc df_17_18.cc historian.cc utility.cc)

target_link_libraries(hello_test GTest::gtest_main)

target_link_libraries(decoder_test GTest::gtest_main glog::glog)

include(GoogleTest)
gtest_discover_tests(decoder_test hello_test)