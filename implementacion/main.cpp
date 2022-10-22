#include "./src/IO.h"
#include "./src/potencia.h"
#include "./src/matriz/matriz_base.h"

int main(int argc,  char** argv) {
    if (argc < 4 || argc > 16) {
        cout << "error: cantidad invalida de parametros.\n" <<
             "expected: [source] [iteraciones] [tolerancia]\n"  <<
             "optional: -f      (formato)           ['grafo' | 'matriz'], default = 'matriz'\n" <<
             "          -x      (vector inicial)    [string]                default = {}" <<
             "          -o      (out dir)           [string],             default = ./\n" <<
             "          -as     (save as)           [string],             default = nombre del source)\n" <<
             "          -p      (precision)         [uint(0, 15)],        default = 15.\n" <<
             "          -time   (tiempo ejecucion)                        default = false\n" <<
             "          -v      (verbose)                                 default = false" << endl;
        return -1;
    }

    // in path
    string in_path = argv[1];
    string file_name = IO::filename(in_path);
    // iteraciones
    size_t niter = IO::stodcast(argv[2], "error: el valor para iterar no se pudo interpretar como entero.");
    // tolerancia
    double tol = IO::stodcast(argv[3], "error: el valor de tolerancia no se pudo interpretar como double.");
    // params opcionales
    map <string, string> params = IO::oparams(argc, argv);
    // out dir
    string out_path = params.count("-o") ? params.at("-o") : "./";
    if (out_path[out_path.length() - 1] != '/') {
        out_path += '/';
    }
    // out name
    string out_name = params.count("-as") ? params.at("-as") : file_name;
    // precision
    int precision = params.count("-p") ?
            IO::stodcast(params.at("-p"), "error: el valor de precision no se pudo interpretar como entero." ) :
            15;
    // formato
    string formato = params.count("-f") ? params.at("-f") : "matriz";

    // read fileIn
    if (params.count("-v")) {
        cout << "leyendo el archivo: " + in_path << ".\n";
    }
    matriz<base> m = formato == "grafo" ?
            grafo_a_matriz<base>(IO::read_grafo(in_path)) :
            IO::read_matriz<base>(in_path);

    // run
    if (params.count("-v")) {
        cout << "calculando autovalores y vectores...\n";
    }
    vector<double> x = {};
    if(params.count("-x")){
        matriz<base> xm = IO::read_matriz<base>(params.at("-x"));
        for(int i = 0; i < xm.m(); ++i) x.push_back(xm.at(0, i));
    }
        
    auto inicio = chrono::high_resolution_clock::now();
    eigen av = potencia(m, niter, tol, x);
    auto fin = chrono::high_resolution_clock::now();

    // write files
    string out = out_path + out_name;
    if (params.count("-v")) {
        cout << "guardando resultado en: " + out << " (si el path existe).\n";
    }
    vector<double> autovalor(m.n(), 0);
    autovalor[0] = av.eigval;
    IO::potencia::write_out(out + ".autovalores.out", autovalor, precision);
    matriz<base> autovector(m.n(), m.n());
    for(int i = 0; i < m.n(); ++i) autovector.set(0, i, av.eigvec[i]);
    IO::write_matriz(out + ".autovectores.out", autovector, precision);

    // time
    if (params.count("-time")) {
        auto time = chrono::duration_cast<chrono::microseconds>(fin - inicio);
        string time_out = out_path + out_name + ".time";
        if (params.count("-v")) {
            cout << "guardando tiempo de ejecucion en: " + time_out << " (si el path existe).\n";
        }
        IO::write_time(time_out, time);
    }
    return 0;
}
