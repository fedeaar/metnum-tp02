#include "src/run.h"


//
// MAIN
//

int main(int argc,  char** argv) {

    if (argc < 4 || argc > 16) {
        cout << "error: cantidad invalida de parametros.\n" <<
             "expected: [source] [iteraciones] [tolerancia]\n"  <<
             "optional: -f      (formato)           ['grafo' | 'matriz'], default = 'matriz'\n" <<
             "          -m      (modo)              ['base' | 'alt'],     default = 'base'\n" <<
             "          -o      (out dir)           [string],             default = './'\n" <<
             "          -as     (save as)           [string],             default = (nombre del source)\n" <<
             "          -p      (precision)         [uint(0, 15)],        default = 15\n" <<
             "          -time   (tiempo ejecucion)                        default = false\n" <<
             "          -v      (verbose)                                 default = false" << endl;
        return -1;
    }

    // == get params ===
    params program = get(argc, argv);

    // == run ===
    if (program.string_params["modo"] == "alt") {
        if (program.bool_params.at("verbose")) cout << "utilizando modo 'alt'" << endl;
        run<alt>(program);
    } else {
        if (program.bool_params.at("verbose")) cout << "utilizando modo 'base'" << endl;
        run<base>(program);
    }

    return 0;
}
