#include "../vector.h"


template<class R>
matriz<R> outer(const vector<double> &a, const vector<double> &b) {
    assert(a.size() == b.size());
    matriz<R> res(a.size(), a.size());
    for(int i = 0; i < a.size(); ++i) {
        for (int j = 0; j < a.size(); ++j) {
            res.set(i, j, a[i] * b[j]);
        }
    }
    return res;
}
