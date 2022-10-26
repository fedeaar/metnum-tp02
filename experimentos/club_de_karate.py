import base.IO as IO
import base.utils as utils

import numpy as np
import pandas as pd


"""
descripcion: 
    evaluación de centralidad de autovector y corte mínimo para el 
    club de karate.

    Nota: correr el experimento regenera todos los archivos, lo que 
    puede resultar en pequeñas discrepancias con los resultados del 
    informe.
"""

#
# IN
#

MATRIZ = "../catedra/karateclub_matriz.txt"
LABELS = "../catedra/karateclub_labels.txt"


# 
# OUT
#

EXPERIMENTO = "club-karate"
DIR_IN, DIR_OUT, DIR = IO.createInOut(EXPERIMENTO, delete=True)

CENTRALIDAD            = DIR + "centralidad.csv"
CENTRALIDAD_COLS       = "nodo,centralidad"
CENTRALIDAD_FMT        = "{0},{1}\n"
ERROR_CENTRALIDAD      = DIR + "error_centralidad.csv"
ERROR_CENTRALIDAD_COLS = "autovalor,error_inf_avect,error_1_avect"
ERROR_CENTRALIDAD_FMT  = "{0},{1},{2}\n"

CORTE_MIN              = DIR + "corte.csv"
CORTE_MIN_COLS         = "autovalor,correlacion"
CORTE_MIN_FMT          = "{0},{1}\n"
ERROR_LAPLACE          = DIR + "error_laplace.csv"
ERROR_LAPLACE_COLS     = "autovalor,error_inf_avect,error_1_avect"
ERROR_LAPLACE_FMT      = "{0},{1},{2}\n"
AUTOVECTORES           = DIR + "karate_laplace.autovectores.txt"
MIN_AUTOVECTOR         = DIR + "karate_laplace.min_autovector.txt"
GRAFO                  = DIR + "grafo_conectividad.png"
GRAFO_CORTE_i          = DIR + "grafo_corte_{i}_{a}.png"


# 
# UTILS
# 

def cortar_grafo(M, v):
    
    A = M.copy()
    for row in range(M.shape[0]):
        for col in range(M.shape[1]):
            if (v[row] > 0) != (v[col] > 0):
                A[row, col] = 0

    return A


# 
# EXPERIMENTOS
#

def medir_centralidad():

    # corremos el metodo
    IO.run(MATRIZ, 20000, 1e-20, o=DIR_OUT)

    # cargamos resultados
    a = np.loadtxt(DIR_OUT + "karateclub_matriz.autovalores.out")
    V = np.loadtxt(DIR_OUT + "karateclub_matriz.autovectores.out")

    # encontramos el maximo
    i = np.nanargmax(a)
    CA = np.round(V[:, i], 6)

    IO.createCSV(CENTRALIDAD, CENTRALIDAD_COLS)
    with open(CENTRALIDAD, 'a', encoding="utf-8") as csv:
        
        for k in range(CA.shape[0]):
            line = CENTRALIDAD_FMT.format(k, CA[k])
            csv.write(line)

    # medimos el error relativo
    M = np.loadtxt(MATRIZ)
    
    IO.createCSV(ERROR_CENTRALIDAD, ERROR_CENTRALIDAD_COLS)
    with open(ERROR_CENTRALIDAD, 'a', encoding="utf-8") as file:
        error = M @ V[:, i] - V[:, i] * a[i]
        error_inf = np.linalg.norm(error, np.inf)
        error_1   = np.linalg.norm(error, 1)
        file.write(ERROR_CENTRALIDAD_FMT.format(a[i], error_inf, error_1))


def medir_corte_minimo():

    # creamos la matriz laplaciana
    M = np.loadtxt(MATRIZ)
    D = np.diag([np.sum(x) for x in M])
    L = D - M

    # corremos el metodo de la potencia
    laplace_file = DIR_IN + "karateclub_laplace.txt"
    np.savetxt(laplace_file, L)
    IO.run(laplace_file, 20000, 1e-20, o=DIR_OUT)
    
    # cargamos resultados
    a = np.loadtxt(DIR_OUT + "karateclub_laplace.autovalores.out")
    V = np.loadtxt(DIR_OUT + "karateclub_laplace.autovectores.out")

    # medimos el error relativo
    error = L @ V - V @ np.diag(a)
    IO.createCSV(ERROR_LAPLACE, ERROR_LAPLACE_COLS)
    with open(ERROR_LAPLACE, 'a', encoding="utf-8") as file:

        for i in range(error.shape[1]):
            
            error_inf = np.linalg.norm(error[:, i], np.inf)
            error_1   = np.linalg.norm(error[:, i], 1)

            line = ERROR_CENTRALIDAD_FMT.format(a[i], error_inf, error_1)
            file.write(line)

    # medimos correlacion de cortes y graficamos
    labels = np.loadtxt(LABELS)
    colores = ['tab:orange' if x else 'tab:blue' for x in labels]

    IO.createCSV(CORTE_MIN, CORTE_MIN_COLS)
    with open(CORTE_MIN, 'a', encoding="utf-8") as csv:

        for i in range(V.shape[0]):  

            corte = cortar_grafo(M, V[:,i])
            
            similaridad = np.round(np.abs(utils.corr(V[:, i], labels)), 6)
            line = CORTE_MIN_FMT.format(np.round(a[i], 6), similaridad)
            csv.write(line)

            path = GRAFO_CORTE_i.format(i=i, a=np.round(a[i], 2))
            utils.graficar_grafo(corte, path,
                size=(10, 10),
                node_size=1000,
                font_size=15, 
                node_color=colores, 
                edge_color='black',
                font_color='white')

    # guardamos autovectores y el minimo
    np.savetxt(AUTOVECTORES, V)

    i = np.nanargmin(a)
    np.savetxt(MIN_AUTOVECTOR, V[:, i], fmt='%1.6f')


# 
# MAIN
#

if __name__ == "__main__":
    
    utils.graficar_grafo(np.loadtxt(MATRIZ), GRAFO, 
        size=(10, 10), 
        node_size=1000, 
        font_size=15, 
        edge_color='black')
        
    medir_centralidad()
    medir_corte_minimo()
