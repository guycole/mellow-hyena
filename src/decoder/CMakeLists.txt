# 
cmake_minimum_required(VERSION 3.10)

project(Decoder)

add_executable(decoder decoder.cc)

#set(VERSION_INFO_MAJOR_VERSION 0) 
#set(VERSION_INFO_MINOR_VERSION 0) 

#set(CMAKE_CXX_STANDARD 11)
#set(CMAKE_CXX_STANDARD_REQUIRED True)

#configure_file(DecoderConfig.h.in DecoderConfig.h)


# TODO 9: Use target_include_directories to include ${PROJECT_BINARY_DIR}
#target_include_directories(Tutorial PUBLIC "${PROJECT_BINARY_DIR}")
#target_include_directories(Tutorial PUBLIC
#                          "${PROJECT_BINARY_DIR}"
#                          "${PROJECT_SOURCE_DIR}/MathFunctions"
#                          )

#add_subdirectory(MathFunctions)
#target_link_libraries(Tutorial PUBLIC MathFunctions)
