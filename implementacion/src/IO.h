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

    map<string, string> oparams(int argc,  char** argv);

    string filename(const string& path);


    /** FILE HANDLING */

    grafo read_grafo(const string &in);

    template<class R> matriz<R> read_matriz(const string &in);

    template<class R> void write_matriz(const string &out, const matriz<R>& mat, int precision=PRECISION);

    void write_time(const string &out, const chrono::microseconds &time);

    pair<size_t, size_t> _shape(const string &in);


    /** POTENCIA */

    namespace potencia {

        struct out_file {
            explicit out_file(unsigned n, unsigned niter, double tol): niter(niter), tol(tol), n(n), solucion() {}

            unsigned n;
            unsigned niter;
            double tol;
            vector<double> solucion;
        };

        out_file read_out(const string &in);

        void write_out_dev(const string &out, unsigned niter, double tol, const vector<double> &res,
                           int precision=PRECISION); // TODO tests

        void write_out(const string &out, const vector<double> &res, int precision=PRECISION);
    }
}


#include "impl/IO.hpp"

#endif //IMPLEMENTACION_IO_H
