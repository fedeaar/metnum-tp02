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
        string param = argv[i];
        if (i + 1 < argc && argv[i+1][0] != '-') {
            string val = argv[i+1];
            params[param] = val;
            ++i;
        } else {
            params[param] = "true";
        }
    }
    return params;
}




//
// FILE HANDLING
//

pair<size_t, size_t> IO::_shape(const string &in) {
    ifstream file {in};
    string _line;
    size_t n {}, m {};
    getline(file, _line);
    if (!_line.empty()) {
        ++n;
        for (char c : _line) {
            m += c == ' ';
        }
        ++m;
    }
    while (getline(file, _line)) {
        ++n;
    }
    return {n, m};
}


grafo IO::read_grafo(const string &in) {
    ifstream file {in};
    if (!file.is_open()) {
        throw std::invalid_argument("no se pudo leer el archivo: " + in + ".");
    }
    // cantidad de nodos
    string _nodos {};
    std::getline(file, _nodos);
    size_t nodos = stodcast(_nodos, "error de formato: linea 1.");
    // cantidad de links
    string _links {};
    std::getline(file, _links);
    size_t links = stodcast(_links, "error de formato: linea 2.");
    // init store
    grafo res(nodos, links);
    // in coords
    string _i, _j;
    size_t i, j, k = 2;
    while (file >> _j >> _i) {
        string msg = "error de formato: linea " + std::to_string(k) + ".";
        i = stolcast(_i, msg);
        j = stolcast(_j, msg);
        res.relaciones.emplace_back(coords{i, j});
        ++k;
    }
    return res;
}


void IO::write_time(const string &out, const chrono::microseconds &time) {
    ofstream file {out};
    file << "microseconds\n" << time.count() << endl;
    file.close();
}




//
// METODO POTENCIA
//

IO::potencia::out_file IO::potencia::read_out(const string &in) {
    ifstream file {in};
    if (!file.is_open()) {
        throw std::invalid_argument("no se pudo leer el archivo: " + in + ".");
    }
    // n
    string _n {};
    std::getline(file, _n);
    size_t n = stodcast(_n, "error de formato: linea 1.");
    // niter
    string _niter {};
    std::getline(file, _niter);
    size_t niter = stodcast(_niter, "error de formato: linea 2.");
    // tol
    string _tol {};
    std::getline(file, _tol);
    double tol = stodcast(_tol, "error de formato: linea 3.");
    // init store
    IO::potencia::out_file params(n, niter, tol);
    // in xi
    string _xi;
    double xi;
    size_t k = 4;
    while (std::getline(file, _xi)) {
        string msg = "error de formato: linea " + std::to_string(k) + ".";
        xi = stodcast(_xi, msg);
        params.solucion.push_back(xi);
    }
    return params;
}


void IO::potencia::write_out_dev(const string &out, unsigned int niter, double tol, const vector<double> &res,
                                int precision) {
    ofstream file {out};
    file << res.size() << '\n' << niter << '\n' << tol << '\n';
    for (auto &xi : res) {
        file << std::setprecision(precision) << std::fixed << xi << '\n';
    }
    file.close();
}


void IO::potencia::write_out(const string &out, const vector<double> &res, int precision) {
    ofstream file {out};
    for (auto &xi : res) {
        file << std::setprecision(precision) << std::fixed << xi << '\n';
    }
    file.close();
}
