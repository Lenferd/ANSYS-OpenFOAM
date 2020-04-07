cmake_minimum_required(VERSION 2.8)

project("Global optimization task scheduler")

message(STATUS "BUILD_CONFIGURATION: ${CMAKE_BUILD_TYPE}")

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/../bin/${CMAKE_BUILD_TYPE}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/../bin/${CMAKE_BUILD_TYPE}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/../bin/${CMAKE_BUILD_TYPE}/)

add_subdirectory(thirdparty)
set(target GOTScheduler)

include_directories(include)

file(GLOB_RECURSE  HEADERS "*.h")
file(GLOB_RECURSE  SOURCES "*.cpp")

add_library(${target} STATIC ${HEADERS} ${SOURCES} src/scheduler.cpp)
