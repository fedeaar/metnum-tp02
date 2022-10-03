#ifndef IMPLEMENTACION_IO_H
#define IMPLEMENTACION_IO_H

#include <chrono>
#include <iomanip>
#include <fstream>
#include <map>

#include "matriz.h"
#include "grafo.h"


namespace IO {

    /** UTILS */

    const int PRECISION = 15;

    size_t stolcast(const string &val, const string &msg);

    double stodcast(const string &val, const string &msg);

    map<string, string> oparams(int argc,  char** argv); // TODO test

    string filename(const string& path);


    /** FILE HANDLING */

    grafo read_grafo(const string &in); // TODO test

    template<class R> matriz<R> read_matriz(const string &in);

    template<class R> void write_matriz(const string &out, const matriz<R>& mat, int precision=PRECISION); // TODO test

    void write_time(const string &out, const chrono::microseconds &time);


    /** POTENCIA */

    namespace potencia {

        struct out_file {
            explicit out_file(unsigned n, unsigned niter, double tol): niter(niter), tol(tol), n(n), solucion(n) {}

            unsigned n;
            unsigned niter;
            double tol;
            vector<double> solucion;
        };

        out_file read_out(const string &in); // TODO test

        void write_out(const string &out, unsigned niter, double tol, const vector<double> &res,
                       int precision=PRECISION); // TODO test
    }
}


#include "impl/IO.hpp"

#endif //IMPLEMENTACION_IO_H
