#ifndef IMPLEMENTACION_POTENCIA_H
#define IMPLEMENTACION_POTENCIA_H

#include "matriz.h"


template<class R>
pair<double, vector<double>> potencia(const matriz<R> &A, size_t niter, double tol);

template<class R>
pair<vector<double>, matriz<R>> deflacion(const matriz<R> &A, size_t k, size_t niter, double tol);


#include "impl/potencia.hpp"

#endif //IMPLEMENTACION_POTENCIA_H
