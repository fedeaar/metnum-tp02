#ifndef IMPLEMENTACION_POTENCIA_H
#define IMPLEMENTACION_POTENCIA_H

#include "matriz.h"
#include "vector.h"


struct eigen
{
    double eigval;
    vector<double> eigvec;
};

size_t MAX_TRIES = 100;

template<class R>
eigen potencia(const matriz<R> &A, size_t niter, double tol, vector<double> x = {});

template<class R>
pair<vector<double>, matriz<R>> deflacion(const matriz<R> &A, size_t k, size_t niter, double tol);


#include "impl/potencia.hpp"

#endif //IMPLEMENTACION_POTENCIA_H
