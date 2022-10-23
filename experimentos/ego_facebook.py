import base.IO as IO
import base.utils as utils

import numpy as np
import pandas as pd

"""
descripcion: 
    Aproximación por matriz de similaridad con producto interno y
    análisis de componentes principales (PCA) para la red ego de 
    Facebook.
"""


# IO
EXPERIMENTO = "ego-facebook"
DIR_IN, DIR_OUT, DIR = IO.createInOut(EXPERIMENTO)


# VARS
GRAFO       = "../catedra/ego-facebook.edges"
CLEAN_GRAFO = DIR_IN + "clean_ego-facebook.conn"
ATRIBUTOS   = "../catedra/ego-facebook.feat"
CLEAN_ATTR  = DIR_IN + "clean_ego-facebook.feat"

# OUTPUT
SIMILARIDAD_RES = DIR + "facebook_similaridad.csv"
SIMILARIDAD_PNG = DIR + "facebook_similaridad.png"
GRAFO_SIM       = DIR_OUT + "grafo_similaridad_{u}.txt"

COLS_SIM = "umbral,flat_corr,av_corr"
FMT_SIM  = "{0},{1},{2}\n"


# UTILS
def clean_data():

    # grafo
    O = IO.readGrafo(GRAFO).astype(int)
    # indexamos
    O = np.insert(O, 0, range(1, O.shape[0]+1), axis=1)
    # del vacios
    O = O[~np.all(O[:,1:] == 0, axis=1)]
    O = O[:, ~np.all(O == 0, axis=0)]

    # atributos
    A = IO.readMatriz(ATRIBUTOS).astype(int)
    # ordenamos
    idx = np.argsort(A[:, 0])
    A = A[idx, :]
    # filtramos solo los que aparecen en O
    A = A[np.in1d(A[:, 0], O[:, 0])]

    assert(np.allclose(A[:, 0], O[:, 0]))

    np.savetxt(CLEAN_GRAFO, O[:, 1:], fmt='%i')
    np.savetxt(CLEAN_ATTR, A[:, 1:], fmt='%i')

    return A[:, 1:], O[:, 1:]


def correlacion_adyacencia(A, O):

    return np.abs(utils.corr(A.flatten(), O.flatten()))


def correlacion_autovalores(A, O):

    w1, V1 = np.linalg.eig(A)
    w2, v2 = np.linalg.eig(O)

    w1 = np.sort(w1)[::-1]
    w2 = np.sort(w2)[::-1]

    return np.abs(utils.corr(w1, w2))


# EXP
def aproximar_similaridad(A, O):

    S = A @ A.T
    umbrales = np.arange(np.max(S))
    
    IO.createCSV(SIMILARIDAD_RES, COLS_SIM)
    with open(SIMILARIDAD_RES, 'a', encoding='utf-8') as file:

        for u in umbrales:
            T = S.copy()
            T = (T > u).astype(int)
            T = T - np.diag(np.diag(T)) # Quito autoconexiones

            np.savetxt(GRAFO_SIM.format(u=u), T, fmt='%i')

            ady = correlacion_adyacencia(T, O)
            av  = correlacion_autovalores(T, O)
            file.write(FMT_SIM.format(u, ady, av))
            print(u, ady, av)


def pca():

    O = IO.readMatriz(CLEAN_GRAFO)
    X = IO.readMatriz(CLEAN_ATTR)

    # Matriz de covarianza
    # col, X = IO.readAtributos(ATRIBUTOS)
    Xcentered = X - X.mean(0)
    n = np.size(Xcentered, 0)
    M = (Xcentered.T@Xcentered) / (n-1)

    # Diagonalizacion de M
    autovals, V = np.linalg.eig(M)
    idx = np.argsort(autovals)[::-1]    # Indexacion para ordenar autovectores segun autovalores   
    autovals = autovals[idx]
    V = V[:,idx]                        # La matriz V se usa para cambio de base
    
    # Observo los diferentes valores de suma acumulada de varianza
    acc = np.cumsum(autovals / np.sum(autovals)).real
    precisiones = np.array([0.5, 0.75, 0.8, 0.85, 0.9, 0.95, 0.99])

    for p in precisiones:
        # Valor de k tal que represento el p%
        k = np.where(acc > p)[0][0]
        # Cambio de base
        A = (X @ V[:, :k]).real
        
        aproximar_similaridad(A, O)



if __name__ == "__main__":

    clean_data()
    
    # O = IO.readMatriz(CLEAN_GRAFO)
    # A = IO.readMatriz(CLEAN_ATTR)
    # aproximar_similaridad(A, O)

    pca()
    
    # df = pd.read_csv(SIMILARIDAD_RES)
    # utils.graficar(
    #     x=df.umbral.to_list() + df.umbral.to_list(),
    #     y=df.flat_corr.to_list() + df.av_corr.to_list(),
    #     hue=["adyacencia estirada"] * len(df.flat_corr) + ["lista de autovalores"] * len(df.av_corr),
    #     xaxis='umbral',
    #     yaxis='correlación',
    #     filename=SIMILARIDAD_PNG
    # )
