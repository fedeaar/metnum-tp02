#ifndef IMPLEMENTACION_POTENCIA_H
#define IMPLEMENTACION_POTENCIA_H

#include "matriz.h"


template<class R>
pair<double, vector<double>> potencia(matriz<R> m, double niter, double tol);


template<class R, class S>
pair<vector<double>, matriz<R>> deflacion(matriz<S> m, unsigned k, double niter, double tol);


#include "impl/potencia.hpp"

#endif //IMPLEMENTACION_POTENCIA_H
