#ifndef POTENCIA_GRAFO_H
#define POTENCIA_GRAFO_H

#include <cstdlib>
#include <vector>

using namespace std;


struct coords {
    coords(size_t _i, size_t _j) : i(_i), j(_j) {}

    size_t i;
    size_t j;
};
struct grafo {
    grafo(size_t _n, size_t _l): nodos(_n), links(_l), relaciones() {}

    size_t nodos;
    size_t links;
    vector<coords> relaciones;
};


#endif //POTENCIA_GRAFO_H