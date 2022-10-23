import base.IO as IO
import base.utils as utils

import numpy as np
import pandas as pd


"""
descripcion: 
    evaluación de centralidad de autovector y corte mínimo para el 
    club de karate.
"""


# IO
EXPERIMENTO = "club-karate"
DIR_IN, DIR_OUT, DIR = IO.createInOut(EXPERIMENTO)

# OUTPUT 
CENTRALIDAD    = f"{DIR}centralidad.csv"
AUTOVECTORES   = f"{DIR}karate_laplace.autovectores.txt"
MIN_AUTOVECTOR = f"{DIR}karate_laplace.min_autovector.txt"
CORTE_MIN      = f"{DIR}corte.csv"
ERROR_LAPLACE  = f"{DIR}error_relativo.csv"
ERROR_CENTRALIDAD = f"{DIR}error_centralidad.csv"
GRAFO          = f"{DIR}grafo_conectividad.png"
GRAFO_CORTE    = DIR + "grafo_corte_{i}_{a}.png"

# VARS
MATRIZ = "../catedra/karateclub_matriz.txt"
LABELS = "../catedra/karateclub_labels.txt"


# UTILS
def cortar_grafo(M, v):
    
    A = M.copy()
    for row in range(M.shape[0]):
        for col in range(M.shape[1]):
            if (v[row] > 0) != (v[col] > 0):
                A[row, col] = 0

    return A


# EXP
def medir_centralidad():

    # corremos el metodo
    IO.run(MATRIZ, 20000, 1e-20, o=DIR_OUT)

    # encontramos el maximo
    a = IO.readAutovalores(f"{DIR_OUT}karateclub_matriz.autovalores.out")
    V = IO.readAutovectores(f"{DIR_OUT}karateclub_matriz.autovectores.out")
    i = np.nanargmax(a)

    # medimos el error
    M = IO.readMatriz(MATRIZ)
    IO.createCSV(ERROR_CENTRALIDAD, "autovalor,error_inf_avect,error_1_avect")
    with open(ERROR_CENTRALIDAD, 'a', encoding="utf-8") as file:
        error = M @ V[:, i] - V[:, i] * a[i]
        error_inf = np.linalg.norm(error, np.inf)
        error_1   = np.linalg.norm(error, 1)
        file.write(f"{a[i]},{error_inf},{error_1}\n")

    # guardamos resultado
    CA = np.round(V[:, i], 6)
    IO.createCSV(CENTRALIDAD, "nodo,centralidad")
    with open(CENTRALIDAD, 'a', encoding="utf-8") as csv:
        csv.write("".join([f"{i},{CA[i]}\n" for i in range(CA.shape[0])]))


def medir_corte_minimo():

    # creamos la matriz laplaciana
    M = IO.readMatriz(MATRIZ)
    D = np.diag([np.sum(x) for x in M])
    L = D - M

    # corremos el metodo de la potencia
    laplace_file = f"{DIR_IN}karateclub_laplace.txt"
    IO.writeMatriz(L, laplace_file)
    IO.run(laplace_file, 20000, 1e-20, o=DIR_OUT)
    
    a = IO.readAutovalores(f"{DIR_OUT}karateclub_laplace.autovalores.out")
    V = IO.readAutovectores(f"{DIR_OUT}karateclub_laplace.autovectores.out")
    
    # medimos el error relativo de los resultados
    error = L @ V - V @ np.diag(a)
    IO.createCSV(ERROR_LAPLACE, "autovalor,error_inf_avect,error_1_avect")
    with open(ERROR_LAPLACE, 'a', encoding="utf-8") as file:
        for i in range(error.shape[1]):
            error_inf = np.linalg.norm(error[:, i], np.inf)
            error_1   = np.linalg.norm(error[:, i], 1)
            file.write(f"{a[i]},{error_inf},{error_1}\n")

    # medimos correlacion de cortes y graficamos
    labels = IO.readMatriz(LABELS)
    colores = ['tab:orange' if x else 'tab:blue' for x in labels]

    IO.createCSV(CORTE_MIN, "autovalor,correlacion")
    with open(CORTE_MIN, 'a', encoding="utf-8") as csv:

        for i in range(V.shape[0]):  
            CORTE = cortar_grafo(M, V[:,i])
            path = GRAFO_CORTE.format(i=i, a=np.round(a[i], 2))
            utils.graficar_grafo(CORTE, path, colores, font_color='white', size=(10, 10), node_size=1000, font_size=15)
            csv.write(f"{np.round(a[i], 6)},{np.round(np.abs(utils.corr(V[:, i], labels)), 6)}\n")

    # guardamos autovectores y el minimo
    IO.writeMatriz(V, AUTOVECTORES)
    i = np.nanargmin(a)
    np.savetxt(MIN_AUTOVECTOR, V[:, i], fmt='%1.6f')




# MAIN
if __name__ == "__main__":
    
    utils.graficar_grafo(IO.readMatriz(MATRIZ), GRAFO, size=(10, 10), node_size=1000, font_size=15)
    medir_centralidad()
    medir_corte_minimo()
