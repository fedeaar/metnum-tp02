#include "../run.h"


//
// PARAMS
//

params get(int argc,  char** argv) {

    string error;
    params res;

    // path
    res.string_params["in_path"] = argv[1];
    string file_name = IO::filename(argv[1]);
    res.string_params["file_name"] = file_name;

    // iteraciones
    error = "error: el valor de iteraciones no se pudo interpretar como entero.";
    res.size_t_params["niter"] = IO::stodcast(argv[2], error);

    // tolerancia
    error =  "error: el valor de tolerancia no se pudo interpretar como double.";
    res.double_params["tol"] = IO::stodcast(argv[3], error);


    // === params opcionales === //

    map <string, string> op = IO::oparams(argc, argv);

    // out dir
    string out_path = op.count("-o") ? op.at("-o") : "./";
    if (out_path[out_path.length() - 1] != '/') {
        out_path += '/';
    }
    res.string_params["out_path"] = out_path;

    // out name
    res.string_params["out_name"] = op.count("-as") ? op.at("-as") : file_name;

    // precision
    error = "error: el valor de precision no se pudo interpretar como entero.";
    res.size_t_params["precision"] = op.count("-p") ? IO::stodcast(op.at("-p"),  error) : 15;

    // formato
    res.string_params["formato"] = op.count("-f") ? op.at("-f") : "matriz";

    // modo
    res.string_params["modo"] = op.count("-m") ? op.at("-m") : "base";

    // verbose
    res.bool_params["verbose"] = op.count("-v");

    // time
    res.bool_params["time"] = op.count("-time");

    return res;
}
