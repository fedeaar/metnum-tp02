#include "../vector.h"


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
    vector<double> res {a};
    for (auto & x: res) {
        x = b / x;
    }
    return res;
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


ostream &operator<<(ostream &os, const vector<double> &v) {
    assert(!v.empty());
    os << '[';
    size_t i = 0;
    while (i < v.size() - 1) {
        os << v[i] << ", ";
        ++i;
    }
    os << v[i] << ']' << endl;
    return os;
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
    bool cero = true;
    for (double & re : res) {
        re = dist(rng);
        cero = cero && re == 0;
    }
    if (cero) { // si res == 0, usamos e1.
        res[0] = 1;
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
    double max = abs(a[0]), tmp;
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
        if (a[j] > a[res]) res = j;
    }
    return res;
}
