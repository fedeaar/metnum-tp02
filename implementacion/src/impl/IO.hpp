#include "../IO.h"


//
// FILE HANDLING
//

template<class R>
matriz<R> IO::read_matriz(const string &in) {
    ifstream file {in};
    if (!file.is_open()) {
        throw std::invalid_argument("no se pudo leer el archivo: " + in + ".");
    }
    // n, m
    pair<size_t, size_t> shape = _shape(in);
    // init
    matriz<R> res(shape.first, shape.second);
    size_t i = 0, j = 0, k = 2;
    string _e {};
    double e {};
    while (file >> _e) {
        string msg = "error de formato: linea " + std::to_string(k) + ".";
        ++k;
        e = stodcast(_e, msg);
        res.set(i, j, e);
        ++j;
        if (j >= shape.second) {
            j = 0;
            ++i;
        }
    }
    return res;
}


template<class R>
void IO::write_matriz(const string &out, const matriz<R> &mat, int precision) {
    ofstream file {out};
    file << std::setprecision(precision) << std::fixed << mat << endl;
    file.close();
}
