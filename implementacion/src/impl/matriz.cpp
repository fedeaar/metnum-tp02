#include "../matriz.h"


//
// VECTOR
//

vector<double> operator*(const vector<double>& a, double b) {
    vector<double> res {a};
    for (auto & x: res) {
        x = x * b;
    }
    return res;
}
vector<double> operator*(double b, const vector<double> &a) {
    return a * b;
}


vector<double> operator/(const vector<double>& a, double b) {
    vector<double> res {a};
    for (auto & x: res) {
        x = x / b;
    }
    return res;
}
vector<double> operator/(double b, const vector<double> &a) {
    return a / b;
}


vector<double> operator+(const vector<double> &a, const vector<double> &b) {
    assert(a.size() == b.size());
    vector<double> res {a};
    for (int i = 0; i < a.size(); ++i) {
        res[i] += b[i];
    }
    return res;
}


vector<double> operator-(const vector<double> &a, const vector<double> &b) {
    assert(a.size() == b.size());
    vector<double> res {a};
    for (int i = 0; i < a.size(); ++i) {
        res[i] -= b[i];
    }
    return res;
}


vector<double> abs(const vector<double> &a) {
    vector<double> res {a};
    for (auto &x : res) {
        x = (x >= 0) ? x : -x;
    }
    return res;
}


double inner(const vector<double> &a, const vector<double> &b) {
    assert(a.size() == b.size());
    double sum = 0;
    for(int i = 0; i < a.size(); ++i) {
        sum += a[i] * b[i];
    }
    return sum;
}


vector<double> aleatorio(size_t n, pair<int, int> range) {
    vector<double> res(n, 0);
    random_device rd;
    mt19937 rng {rd()}; // Mersenne Twister
    uniform_int_distribution<int> dist(range.first, range.second);
    for (double & re : res) {
        re = dist(rng);
    }
    return res;
}


vector<double> normalizar(const vector<double> &v) {
    double n = sqrt(inner(v, v));
    return abs(n) < EPSILON ? v : v / n;
}


bool eq(const vector<double> &a, const vector<double> &b, double epsilon) {
    bool res = a.size() == b.size();
    for (size_t i = 0; i < a.size() && res; ++i) {
        res = abs(a[i] - b[i]) < epsilon;
    }
    return res;
}


double inf(const vector<double> &a) {
    assert(!a.empty());
    double max = a[0], tmp;
    for (auto x : a) {
        tmp = abs(x);
        if (tmp > max) {
            max = tmp;
        }
    }
    return max;
}


size_t maxarg(const vector<double> &a) {
    size_t res = 0;
    for (size_t j = 0; j < a.size(); ++j) {
        if(a[j] > a[res]) res = j;
    }
    return res;
}
