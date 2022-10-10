#include "../potencia.h"


//
// METODO POTENCIA
//

// TODO que hacemos si x queda ortogonal a v1
template<class R>
pair<double, vector<double>> potencia(const matriz<R> &A, size_t niter, double tol) {
    size_t n = A.n();
    vector<double> cero(n, 0);

    // elegimos x
    vector<double> x = aleatorio(n);
    if (eq(x, cero)) { // si x ~= 0, usamos e1.
        x = cero;
        x[0] = 1;
    } else {
        normalizar(x);
    }

    // estimamos el autovector
    vector<double> y, z;
    size_t i = 0;
    while (i++ < niter) {
        y = A * (A * x);
        if (eq(y, cero)) {
            break;
        }
        y = y / sqrt(inner(y, y));
        z = x - y;
        if (sqrt(inner(z, z)) < tol) {
            break;
        }
        x = y;
    }

    // estimamos el autovalor
    double a = inner(x, A * x) / inner(x, x);

    return {a, x};
}

//
//template<class R>
//pair<vector<double>, matriz<R>> Hdeflacion(const matriz<R> &A, size_t k, size_t niter, double tol) {
//    size_t n = A.n();
//    matriz<R> B = A;
//    vector<double> eigvals;
//    matriz<R> eigvecs(n, k);
//
//    for (size_t i = 0; i < k; ++i) {
//        pair<double, vector<double>> av = potencia(B, niter, tol);
//        eigvals.emplace_back(av.first);
//        for (size_t j = 0; j < n; ++j) {
//            eigvecs.set(j, i, av.second[j]);
//        }
//        B = B - av.first * outer<R>(av.second, av.second);
//    }
//    return {eigvals, eigvecs};
//}

template<class R>
pair<vector<double>, matriz<R>> deflacion(const matriz<R> &A, size_t k, size_t niter, double tol) {
    size_t n = A.n();
    matriz<R> B = A;
    vector<double> eigvals;
    matriz<R> eigvecs(n, k);

    for (size_t i = 0; i < k; ++i) {
        pair<double, vector<double>> av = potencia(B, niter, tol);
        eigvals.emplace_back(av.first);

        for (size_t j = 0; j < n; ++j) {
            eigvecs.set(j, i, av.second[j]);
        }

        size_t mxpos = 0;
        for (size_t j = 0; j < n; ++j) {
            if(abs(av.second[j]) > abs(av.second[mxpos])) mxpos = j;
        }

        vector<double> x(n, 0);
        x[0] = 1/(av.first * av.second[mxpos]);
        x = A * x;

        B = B - av.first * outer<R>(av.second, x);
    }
    return {eigvals, eigvecs};
}
