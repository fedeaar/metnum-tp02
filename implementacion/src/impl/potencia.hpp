#include "../potencia.h"


//
// METODO POTENCIA
//


template<class R>
eigen potencia(const matriz<R> &A, size_t niter, double tol) {
    assert(!A.empty());
    niter = (size_t) niter / 2;
    size_t n = A.n();
    matriz<R> B = A * A;
    vector<double> cero(n, 0);
    vector<double> x, y, z;
    bool ortogonal;
    do {
        ortogonal = false;
        x = normalizar(aleatorio(n));
        for (size_t i = 0; i < niter; ++i) {
            y = B * x;
            if (eq(y, cero)) {
                ortogonal = true;
                break;
            }
            y = normalizar(y);
            z = x - y;
            if (sqrt(inner(z, z)) < tol) {
                break;
            }
            x = y;
        }
    } while (ortogonal);
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
   // cout << eigvals << endl;
   return {eigvals, eigvecs};
}

// template<class R>
// pair<vector<double>, matriz<R>> deflacion(const matriz<R>& A, size_t k, size_t niter, double tol) {
//     size_t n = A.n();
//     vector<double> eigvals;
//     matriz<R> eigvecs(n, k);

//     matriz<R> B = A;
//     vector<double> x = aleatorio(n);
//     for (size_t i = 0; i < k; ++i, --n) {
//         pair<double, vector<double>> av = potencia(B, niter, tol, x);
//         eigvals.emplace_back(av.eigval);


//         for (size_t j = 0; j < n; ++j) {
//             eigvecs.set(j, i, av.eigvec[j]);
//         }

//         matriz<R> C(n-1, n-1);
//         size_t mxpos = maxarg(abs(av.eigvec));
//         for(int k = 0; k < mxpos; ++k)
//             for(int j = 0; j < mxpos; ++j)
//                 C.set(k, j, A.at(k, j) - av.eigvec[k] * A.at(mxpos, j) / av.eigvec[mxpos]);
            

//         for(int k = mxpos; k < n-1; ++k)
//             for(int j = 0; j < mxpos; ++j){
//                 C.set(k, j, A.at(k+1, j) - av.eigvec[k+1] * A.at(mxpos, j) / av.eigvec[mxpos]);
//                 C.set(j, k, A.at(j, k+1) - av.eigvec[j] * A.at(mxpos, k+1) / av.eigvec[mxpos]);
//             }
        
//         for(int k = mxpos; k < n-1; ++k)
//             for(int j = mxpos; j < n-1; ++j)
//                 C.set(k, j, A.at(k+1, j+1) - av.eigvec[k+1] * A.at(mxpos, j+1) / av.eigvec[mxpos]);
        
//         B = C;

//     }
//     return {eigvals, eigvecs};
// }

// template<class R>
// pair<vector<double>, matriz<R>> deflacion(const matriz<R>& A, size_t k, size_t niter, double tol) {
//     size_t n = A.n();
//     vector<double> eigvals;
//     matriz<R> eigvecs(n, k);
//
//     matriz<R> B = A;
//     vector<double> x = aleatorio(n);
//     for (size_t i = 0; i < k; ++i) {
//         eigen av = potencia(B, niter, tol, aleatorio(n));
//         eigvals.emplace_back(av.eigval);
//
//
//         for (size_t j = 0; j < n; ++j) {
//             eigvecs.set(j, i, av.eigvec[j]);
//         }
//         size_t mxpos = maxarg(abs(av.eigvec));
//
//         fill(x.begin(), x.end(), 0);
//         x[mxpos] = 1/av.eigvec[mxpos];
//         x = (x * B);
//         B = B - outer<R>(av.eigvec, x);
//     }
//     return {eigvals, eigvecs};
// }
