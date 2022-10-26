#ifndef POTENCIA_RUN_H
#define POTENCIA_RUN_H

#include "IO.h"
#include "potencia.h"
#include "matriz/matriz_base.h"
#include "matriz/matriz_alt.h"


struct params {
    map<string, string> string_params {};
    map<string, double> double_params {};
    map<string, size_t> size_t_params {};
    map<string, bool>   bool_params {};
};


params get(int argc,  char** argv);


template<class R>
void run(const params &program);


# include "impl/run.hpp"

#endif //POTENCIA_RUN_H
