
//
// RUN
//

template<class R>
void run(const params &program) {

    bool verbose = program.bool_params.at("verbose");

    // read
    bool grafo = program.string_params.at("formato") == "grafo";
    string in_path =  program.string_params.at("in_path");
    if (verbose) cout << "leyendo el archivo (como " << (grafo ? "grafo" : "matriz") << "): " + in_path << "\n";
    matriz<R> m = grafo ? grafo_a_matriz<R>(IO::read_grafo(in_path)) : IO::read_matriz<R>(in_path);

    // calcular
    if (verbose) cout << "calculando autovalores y vectores...\n";
    auto inicio = chrono::high_resolution_clock::now();
    pair<vector<double>, matriz<R>> av = deflacion(m, m.n(), program.size_t_params.at("niter"),
                                                     program.double_params.at("tol"));
    auto fin = chrono::high_resolution_clock::now();
    auto time = chrono::duration_cast<chrono::microseconds>(fin - inicio);
    if (verbose) cout << "tiempo de ejecucion (microsegundos): " << time.count() << '\n';

    // write
    string out = program.string_params.at("out_path") + program.string_params.at("out_name");
    int precision = program.size_t_params.at("precision");
    if (verbose) cout << "guardando resultados en: " << out << ".{ autovalores, autovectores }.out (si el path existe)\n";
    IO::potencia::write_out(out + ".autovalores.out", av.first, precision);
    IO::write_matriz(out + ".autovectores.out", av.second, precision);

    // write time
    if (program.bool_params.at("time")) {
        string time_out = out + ".time";
        if (verbose) cout << "guardando tiempo de ejecucion en: " + time_out << " (si el path existe)" << endl;
        IO::write_time(time_out, time);
    }
}
