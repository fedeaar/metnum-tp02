#ifndef IMPLEMENTACION_IO_H
#define IMPLEMENTACION_IO_H

#include <chrono>
#include <iomanip>
#include <fstream>
#include <map>


namespace IO {

    /** UTILS */

    const int PRECISION = 15;

    size_t stolcast(const string &val, const string &msg);

    double stodcast(const string &val, const string &msg);

    map<string, string> oparams(int argc,  char** argv);

    string filename(const string& path);
}


#endif //IMPLEMENTACION_IO_H
