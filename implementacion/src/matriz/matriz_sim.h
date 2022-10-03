#ifndef IMPLEMENTACION_MATRIZ_ALT_H
#define IMPLEMENTACION_MATRIZ_ALT_H

#include "../matriz.h"
#include "matriz_alt.h"

using namespace std;

class sim {
protected: 
    matriz<alt> _mat;   // matriz

public:
    /** CONSTRUCTOR */
    sim(size_t n, size_t m);

    /** INTERFAZ */
    double at(size_t row, size_t col) const;
    void set(size_t row, size_t col, double val);

    //** ITERADORES */
};



#endif //IMPLEMENTACION_MATRIZ_ALT_H
