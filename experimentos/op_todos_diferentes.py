import base.IO as IO
import base.utils as utils
from base.utils import n2 as n2

import numpy as np
import pandas as pd


"""
    Este experimento se encarga de observar si el método de 
    la potencia converge en el caso más sencillo que es
    cuando el autovalor dominante no esta repetido.

    Nota: correr el experimento regenera todos los archivos, lo que 
    puede resultar en pequeñas discrepancias con los resultados del 
    informe.
"""


# 
# IO
#

EXPERIMENTO = "op_todos-diferentes"
DIR_IN, DIR_OUT, DIR = IO.createInOut(EXPERIMENTO, delete=True)
RES = f"{DIR}{EXPERIMENTO}.csv"
MATRIZ_IN     = f"{DIR_IN}matriz.txt"
X_IN          = f"{DIR_IN}x.txt"
AVECS_EXPECTED = f"{DIR_IN}avecs_exp.txt"
AVALS_EXPECTED = f"{DIR_IN}avals_exp.txt"

SUMMARY   = f"{DIR}{EXPERIMENTO}_summary.csv"
GRAFICO_AVAL = f"{DIR}{EXPERIMENTO}_val.png"
GRAFICO_AVEC = f"{DIR}{EXPERIMENTO}_vec.png"

COLS       = 'iter,error_autovalor,error_n2_autovectores'
FMT_COLS   = "{0},{1},{2}\n"


# 
# VARIABLES
#
N = 20
NITER = 100
STEP = 1 # tiene que se par para que tenga sentido
TOL = 0


#
# UTILS
#

def make_tests():
    
    print('creando test...')    
    # nos aseguramos de que el autovalor maximo no este repetido
    # los demás autovalores si pueden estar repetidos
    S, V, a = utils.armarMatriz([N], N)
    x = utils.armarRandom(N)
    np.savetxt(MATRIZ_IN, S)
    np.savetxt(AVALS_EXPECTED, a)
    np.savetxt(X_IN, x)
    np.savetxt(AVECS_EXPECTED, V)
    return S, x


def pathAval(i):
    return f"{DIR_OUT}t_{i}_autovalor.out"


def pathAvec(i):
    return f"{DIR_OUT}t_{i}_autovector.out"


# 
# RUN
#

def run_tests():
    S, x = make_tests()

    print(f'corriendo iteracion: {0}') 
    a, x = utils.metodo_potencia(S, 0, TOL, np.reshape(x, (N, 1)))
    np.savetxt(pathAvec(0), x)
    np.savetxt(pathAval(0), [a])

    for i in range(STEP, NITER+1, STEP):
        print(f'corriendo iteracion: {i}') 
        a, x = utils.metodo_potencia(S, STEP, TOL, np.reshape(x, (N, 1)))
        np.savetxt(pathAvec(int(i/STEP)), x)
        np.savetxt(pathAval(int(i/STEP)), [a])


def eval_tests():
    
    with open(RES, 'a', encoding="utf-8") as file:
        e = np.loadtxt(AVALS_EXPECTED)
        e = e[0]
        Q = np.loadtxt(AVECS_EXPECTED)
        q_d = Q.T[0]
        vf = np.loadtxt(pathAvec( int(NITER/STEP) ))


        # hay 2 posibles autovectores de norma2 = 1 a los que puede converger
        # seteamos invertido para chequear que converga a alguno de los 2
        invertido = False
        if(np.allclose(vf, -q_d, 0.2)): 
            invertido = True

        for i in range(int(NITER/STEP)+1):
            print(f'evaluando resultados: {i}') 

            a = np.loadtxt(pathAval(i))
            error = abs(a - e)

            v = np.loadtxt(pathAvec(i))
            norma2 = n2(v - q_d)
            if invertido: norma2 = 2 - norma2 

            file.write(FMT_COLS.format(i*STEP, error, norma2))


#
# MAIN
#

if __name__ == "__main__":

    run_tests()
    IO.createCSV(RES, COLS)
    eval_tests()

    df = pd.read_csv(RES)
    df.describe().to_csv(SUMMARY)
    
    utils.graficar(
        x=df.iter, 
        y=df.error_n2_autovectores, 
        hue=["caso testigo"]*(int(NITER/STEP) + 1), 
        xaxis="CANTIDAD DE ITERACIONES", 
        yaxis="ERROR", 
        filename=GRAFICO_AVEC)

    utils.graficar(
        x=df.iter, 
        y=df.error_autovalor,
        hue=["caso testigo"]*(int(NITER/STEP) + 1), 
        xaxis="CANTIDAD DE ITERACIONES", 
        yaxis="ERROR", 
        filename=GRAFICO_AVAL)
