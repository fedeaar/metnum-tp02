cmake_minimum_required(VERSION 3.16)
project(potencia)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread -std=gnu++14 -ggdb3 -g")

add_library(gtest STATIC tests/gtest-1.8.1/gtest-all.cc)
add_library(gtest_main STATIC tests/gtest-1.8.1/gtest_main.cc)

set(SOURCE_FILES
        src/matriz.h
        src/matriz/matriz_base.h
        src/matriz/matriz_alt.h
        # src/matriz/matriz_sim.h
        src/impl/matriz.hpp
        src/impl/matriz/matriz_base.cpp
        src/impl/matriz/matriz_alt.cpp
        # src/impl/matriz/matriz_sim.cpp
        src/vector.h
        src/impl/vector.hpp
        src/impl/vector.cpp
        src/grafo.h
        src/potencia.h
        src/impl/potencia.hpp
        src/IO.h
        src/impl/IO.cpp
        src/run.h
        src/impl/run.hpp
        src/impl/run.cpp)
        

add_executable(TESTS-matriz-base ${SOURCE_FILES} tests/matriz-tests.cpp)
target_compile_definitions(TESTS-matriz-base PUBLIC ESTR=1)
target_link_libraries(TESTS-matriz-base gtest gtest_main)

add_executable(TESTS-potencia ${SOURCE_FILES} tests/potencia-tests.cpp)
target_link_libraries(TESTS-potencia gtest gtest_main)

add_executable(tp2 ${SOURCE_FILES} main.cpp)
