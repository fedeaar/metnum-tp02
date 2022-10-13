import base.IO as IO
import base.utils as utils

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


"""
descripcion: 
    evaluación de centralidad de autovector y partición para el 
    club de karate.
"""


# IO
EXPERIMENTO = "club-karate"
DIR_IN, DIR_OUT, DIR = IO.createInOut(EXPERIMENTO)

# archivos de resultados    
CENTRALIDAD = f"{DIR}{EXPERIMENTO}_centralidad.txt"
CORTES      = f"{DIR}{EXPERIMENTO}_cortes.txt"
CORTES_MIN  = f"{DIR}{EXPERIMENTO}_cortes_min.txt"
GRAFICO     = f"{DIR}{EXPERIMENTO}.png"

# variables
KARATE = IO.readMatriz("../catedra/karateclub_matriz.txt")
LABELS = IO.readMatriz("../catedra/karateclub_labels.txt")



# utils
def corr(x, y, epsilon=1e-16):
    xc = x - x.mean()
    yc = y - y.mean()
    a = xc.T @ yc
    b = np.sqrt((xc**2).T @ (yc**2))
    return a / b if abs(b) >= epsilon else 0


# metodos
def grafo():
    G = nx.from_numpy_array(KARATE)
    f = plt.figure(figsize=(10, 10))
    nx.draw(G, with_labels=True, ax=f.add_subplot())
    f.savefig(GRAFICO)


def centralidad():
    w, V = np.linalg.eigh(KARATE)  # TODO: utilizar ./tp2
    i = np.argmax(w)
    IO.writeMatriz(V[:, i], CENTRALIDAD)


def laplace():
    D = np.diag([np.sum(x) for x in KARATE])
    L = D - KARATE
    w, V = np.linalg.eigh(L)  # TODO: utilizar ./tp2

    mi, mw, mc = 0, w[0], abs(corr(V[:, 0], LABELS))
    for i in range(V.shape[0]):
        tmp = corr(V[:, i], LABELS)
        if abs(tmp) > mc:
            mi, mw, mc = i, w[i], tmp

    IO.writeMatriz(V, CORTES)
    IO.writeMatriz(V[:, mi], CORTES_MIN)




if __name__ == "__main__":
    
    grafo()
    centralidad()
    laplace()
