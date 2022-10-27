import base.IO as IO
import base.utils as utils
from base.utils import n2 as n2

import numpy as np
import pandas as pd


"""
    Este experimento se encarga de observar si el método de la potencia 
    converge  y a que autovalor converge en caso de que el autovalor 
    dominante de la matriz este repetido.
    No tiene sentido chequear a que autovector converge ya que al estar 
    repetido el autovalor hay infinitas opciones y puede no converger 
    a la misma que dice numpy.

    Nota: correr el experimento regenera todos los archivos, lo que 
    puede resultar en pequeñas discrepancias con los resultados del 
    informe.
"""


# 
# OUT
#

EXPERIMENTO = "op_autovalor-repetido"
DIR_IN, DIR_OUT, DIR = IO.createInOut(EXPERIMENTO, delete=True)

RES = f"{DIR}{EXPERIMENTO}.csv"
MATRIZ_IN     = f"{DIR_IN}matriz.txt"
X_IN          = f"{DIR_IN}x.txt"
AVECS_EXPECTED = f"{DIR_IN}avecs_exp.txt"
AVALS_EXPECTED = f"{DIR_IN}avals_exp.txt"

SUMMARY   = f"{DIR}{EXPERIMENTO}_summary.csv"
GRAFICO_AVAL = f"{DIR}{EXPERIMENTO}_val.png"

COLS       = 'iter,error_autovalor'
FMT_COLS   = "{0},{1}\n"


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
    
    S, V, a = utils.armarMatriz([N, N], N) #nos aseguramos de que haya un autovalor repetido
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
        np.savetxt(pathAval(int(i/STEP)), [a])


def eval_tests():
    # importo los autovalores esperados
    e = np.loadtxt(AVALS_EXPECTED)
    e = e[0]

    with open(RES, 'a', encoding="utf-8") as file:
        for i in range(int(NITER/STEP)+1):
            print(f'evaluando resultados: {i}') 

            a = np.loadtxt(pathAval(i))
            error = abs(a - e)

            file.write(FMT_COLS.format(i*STEP, error))


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
        y=df.error_autovalor,
        hue=["distancia al autovalor esperado"]*(int(NITER/STEP) + 1), 
        xaxis="cantidad de iteraciones", 
        yaxis="error", 
        filename=GRAFICO_AVAL)
