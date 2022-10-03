#include "../../matriz/matriz_sim.h"




//
// ALT
//

sim::sim(size_t n, size_t m):  _mat(n, m){}


double sim::at(size_t row, size_t col) const {
    if(col > row) 
        return _mat.at(col, row);
    else 
        return _mat.at(row, col);
}


void sim::set(size_t row, size_t col, double val) {
    if(row < col) 
        _mat.set(col, row, val);
    else 
        _mat.set(row, col, val);
}




