#include "../IO.h"


//
// UTILS
//

size_t IO::stolcast(const string &val, const string &msg) {
    size_t res;
    try {
        res = std::stoll(val);
    } catch(std::invalid_argument &ia) {
        throw std::invalid_argument(msg);
    }
    return res;
}


double IO::stodcast(const string &val, const string &msg) {
    double res;
    try {
        res = std::stod(val);
    } catch(std::invalid_argument &ia) {
        throw std::invalid_argument(msg);
    }
    return res;
}


string IO::filename(const string &path) {
    string name;
    // encontrar nombre
    auto delim = path.find_last_of('/');
    if (delim != string::npos) {
        name = path.substr(delim + 1, path.size());
    } else {
        name = path;
    }
    // remover extension
    delim = name.find_last_of('.');
    if (delim != string::npos) {
        name = name.substr(0, delim);
    }
    return name;
}


map<string, string> IO::oparams(int argc,  char** argv) {
    map<string, string> params;
    for (int i = 0; i < argc; ++i) {
        if (argv[i][0] != '-') {
            continue;
        }
        string arg = argv[i];
        string param;
        string val;
        auto delim = arg.find('=');
        if (delim != string::npos) {
            param = arg.substr(0, delim);
            val = arg.substr(delim + 1, arg.size());
        } else {
            param = arg;
            val = "true";
        }
        params[param] = val;
    }
    return params;
}
