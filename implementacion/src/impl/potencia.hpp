#include "../potencia.h"


//
// METODO POTENCIA
//


template<class R>
eigen potencia(const matriz<R> &A, size_t niter, double tol) {

    double e = tol;
    niter = (size_t) (niter / 2);

    vector<double> x, y, z;
    x = normalizar(aleatorio(A.n()));

    for (size_t i = 0; i < niter && e >= tol; ++i) {
        y = A * (A * x);
        y = normalizar(y);
        z = x - y;
        x = y;
        e = sqrt(inner(z, z));
    }

    double a = inner(x, A * x) / inner(x, x);
    return {a, x};
}


template<class R>
pair<vector<double>, matriz<R>> deflacion(const matriz<R> &A, size_t k, size_t niter, double tol) {

   size_t n = A.n();
   matriz<R> B = A;

   vector<double> eigvals;
   matriz<R> eigvecs(n, k);

   for (size_t i = 0; i < k; ++i) {
       eigen av = potencia(B, niter, tol);
       eigvals.emplace_back(av.eigval);
       for (size_t j = 0; j < n; ++j) {
           eigvecs.set(j, i, av.eigvec[j]);
       }
       B = B - av.eigval * outer<R>(av.eigvec, av.eigvec);
   }

   return {eigvals, eigvecs};
}
