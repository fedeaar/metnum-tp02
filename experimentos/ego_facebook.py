import base.IO as IO
import base.utils as utils

import numpy as np
import pandas as pd

"""
descripcion: 
    Aproximación por matriz de similaridad con producto interno y
    análisis de componentes principales (PCA) para la red ego de 
    Facebook.

    Nota: correr el experimento regenera todos los archivos, lo que 
    puede resultar en pequeñas discrepancias con los resultados del 
    informe.
"""


#
# IN
#

GRAFO       = "../catedra/ego-facebook.edges"
ATRIBUTOS   = "../catedra/ego-facebook.feat"


# 
# OUT
#

EXPERIMENTO = "ego-facebook"
DIR_IN, DIR_OUT, DIR = IO.createInOut(EXPERIMENTO, delete=True)

CLEAN_GRAFO      = DIR + "clean_ego-facebook.conn"
CLEAN_ATTR       = DIR + "clean_ego-facebook.feat"

SIMILARIDAD_RES  = DIR + "facebook_similaridad.csv"
SIMILARIDAD_COLS = "umbral,flat_corr,av_corr,mean_corr,aciertos,aciertos_pct,desaciertos,desaciertos_pct"
SIMILARIDAD_FMT  = "{0},{1},{2},{3},{4},{5},{6},{7}\n"
SIMILARIDAD_PLOT = DIR + "facebook_similaridad.png"

PCA_RES          = DIR + "facebook_similaridad_pca.csv"
PCA_COLS         = "p,umbral,flat_corr,av_corr,mean_corr,aciertos,aciertos_pct,desaciertos,desaciertos_pct"
PCA_FMT          = "{0},{1},{2},{3},{4},{5},{6},{7},{8}\n"
PCA_MATRIZ       = DIR_OUT + "grafo_similaridad_PCA_{u}_{p}.txt"
PCA_PLOT         = DIR + "facebook_similaridad_PCA.png"

UMBRAL_MATRIZ    = DIR_OUT + "grafo_similaridad_{u}.txt"
UMBRAL_GRAFO     = DIR + "grafo_{name}.png"


#
# UTILS
#

def clean_data():

    # grafo
    O = IO.read_adylist(GRAFO).astype(int)
    # indexamos
    O = np.insert(O, 0, range(1, O.shape[0]+1), axis=1)
    # del vacios
    O = O[~np.all(O[:,1:] == 0, axis=1)]
    O = O[:, ~np.all(O == 0, axis=0)]

    # atributos
    A = np.loadtxt(ATRIBUTOS).astype(int)
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


def correlacion_promedio(A, O):
    
    A = A.flatten()
    O = O.flatten()
    total = O.size
    return (np.count_nonzero(A == O) / total)


def conexiones_acertadas(A, O):
    
    aux = np.where(O == 0, -1, O)
    bien = np.where((aux - A) == 0, 1, 0)
    extras = np.where((aux - A) == -2, 1, 0)

    bien = np.count_nonzero(bien) / 2
    extras = np.count_nonzero(extras) / 2
    total = np.count_nonzero(A)
    return bien, bien / total if total else 0, extras, extras / total if total else 0


#
# EXPERMIENTOS
#

def aproximar_similaridad(A, O, filename_csv, p=None):

    S = A @ A.T
    umbrales = np.arange(np.max(S))
    
    with open(filename_csv, 'a', encoding='utf-8') as file:

        for u in umbrales:
            T = S.copy()
            T = (T > u).astype(int)
            T = T - np.diag(np.diag(T)) # Quito autoconexiones
            
            if p:
                file_matriz = PCA_MATRIZ.format(u=u, p=p)
            else:
                file_matriz = UMBRAL_MATRIZ.format(u=u)
            np.savetxt(file_matriz.format(u=u, p=p), T, fmt='%i')

            ady = correlacion_adyacencia(T, O)
            av  = correlacion_autovalores(T, O)
            cc  = correlacion_promedio(T, O)
            b, bp, m, mp = conexiones_acertadas(T, O)

            if p:
                line = PCA_FMT.format(p, u, ady, av, cc, b, bp, m, mp)
            else:
                line = SIMILARIDAD_FMT.format(u, ady, av, cc, b, bp, m, mp)
            file.write(line)
            
            
def pca():

    O = np.loadtxt(CLEAN_GRAFO)
    X = np.loadtxt(CLEAN_ATTR)

    # Matriz de covarianza
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

    IO.createCSV(PCA_RES, PCA_COLS)
    for p in precisiones:
        # Valor de k tal que represento el p%
        k = np.where(acc > p)[0][0]
        # Cambio de base
        A = (X @ V[:, :k]).real
        
        aproximar_similaridad(A, O, PCA_RES, p)


#
# MAIN
#

if __name__ == "__main__":

    A, O = clean_data()

    IO.createCSV(SIMILARIDAD_RES, SIMILARIDAD_COLS)
    aproximar_similaridad(A, O, SIMILARIDAD_RES)

    pca()

    df = pd.read_csv(SIMILARIDAD_RES)
    l = len(df.umbral)
    utils.graficar(
        x=df.umbral.to_list() * 3,
        y=df.flat_corr.to_list() + 
          df.av_corr.to_list() +
          df.mean_corr.to_list(),
        hue=["adyacencia estirada"] * l +
            ["lista de autovalores"] * l +
            ["posiciones coincidentes"] * l,
        xaxis='umbral',
        yaxis='correlación',
        filename=SIMILARIDAD_PLOT
    )

    df = pd.read_csv(PCA_RES)
    l = len(df.umbral)
    utils.graficar(
        x=df.umbral.to_list() * 3,
        y=df.flat_corr.to_list() + 
          df.av_corr.to_list() +
          df.mean_corr.to_list(),
        hue=["adyacencia estirada"] * l +
            ["lista de autovalores"] * l +
            ["posiciones coincidentes"] * l,
        xaxis='umbral',
        yaxis='correlación',
        filename=PCA_PLOT,
        units=df.p.to_list() * 3
    )

    for i in range(15):
        grafo = CLEAN_GRAFO if i == 0 else UMBRAL_MATRIZ.format(u=f"{i}.0")
        A = IO.readMatriz(grafo)
        utils.graficar_grafo(A, 
            UMBRAL_GRAFO.format(name=(i if i != 0 else 'facebook')), 
            node_color='tab:blue', 
            edge_color='darkgray',
            size=(20, 20), 
            node_size=300, 
            with_labels=False)
