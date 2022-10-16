#ifndef POTENCIA_VECTOR_H
#define POTENCIA_VECTOR_H

#include <vector>
#include <random>

#include "matriz.h"


using namespace std;


double inner(const vector<double> &a, const vector<double> &b);

template<class R>
matriz<R> outer(const vector<double> &a, const vector<double> &b);

vector<double> operator*(const vector<double>& a, double b); // TODO test
vector<double> operator*(double b, const vector<double> &a);

vector<double> operator/(const vector<double>& a, double b); // TODO test
vector<double> operator/(double b, const vector<double> &a);

vector<double> operator+(const vector<double> &a, const vector<double> &b); // TODO test

vector<double> operator-(const vector<double> &a, const vector<double> &b); // TODO test

ostream &operator<<(ostream &os, const vector<double> &v); // TODO test

vector<double> abs(const vector<double> &a); // TODO test

vector<double> aleatorio(size_t n, pair<int, int> range={INT32_MIN, INT32_MAX}); // TODO test

vector<double> normalizar(const vector<double> &v); // TODO test

bool eq(const vector<double> &a, const vector<double> &b, double epsilon=EPSILON); // TODO test

double inf(const vector<double> &a); // TODO test

size_t maxarg(const vector<double> &a); // TODO test


#include "impl/vector.hpp"

#endif //POTENCIA_VECTOR_H
