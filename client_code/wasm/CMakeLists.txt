cmake_minimum_required(VERSION 3.10)
project(video_processor)

# Set C++ standard
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Ensure we're using Emscripten compiler
if(NOT DEFINED ENV{EMSCRIPTEN})
    message(FATAL_ERROR "This project must be compiled with Emscripten. Please run cmake with emcmake.")
endif()

# Set output directory
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})

# Add include directories
include_directories(${CMAKE_SOURCE_DIR}/src)

# Define the WebAssembly output file
add_executable(video_processor src/video_processor.cpp)

# Set Emscripten-specific compiler flags
set_target_properties(video_processor PROPERTIES
    LINK_FLAGS "-s WASM=1 -s ALLOW_MEMORY_GROWTH=1 -s EXPORTED_RUNTIME_METHODS=['cwrap'] -s EXPORTED_FUNCTIONS=['_processVideoFrame','_malloc','_free'] -s MODULARIZE=1 -s EXPORT_NAME='VideoProcessorModule' --bind"
    OUTPUT_NAME "video_processor"
)

# Custom command to copy the built files to the theme directory
add_custom_command(TARGET video_processor POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy
    ${CMAKE_BINARY_DIR}/video_processor.js
    ${CMAKE_BINARY_DIR}/video_processor.wasm
    ${CMAKE_SOURCE_DIR}/../../../theme/wasm/
) 