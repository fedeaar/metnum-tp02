#include "../grafo.h"

template<class R>
matriz<R> grafo_a_matriz(const grafo &g) {
    matriz<R> res (g.nodos, g.nodos);
    for (auto &r: g.relaciones) {
        if (r.i != r.j) {
            res.set(r.i - 1, r.j - 1, 1);
        }
    }
    return res;
}
