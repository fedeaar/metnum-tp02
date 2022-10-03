#include "../matriz.h"


double inner(const vector<double> &a, const vector<double> &b) {
    assert(a.size() == b.size());
    double sum = 0;
    for(int i = 0; i < a.size(); ++i) {
        sum += a[i] * b[i];
    }
    return sum;
}
