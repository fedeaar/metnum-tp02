import base.IO as IO
import base.utils as utils
from base.utils import n2 as n2, random_matriz

import numpy as np
import pandas as pd


"""
    Este experimento se encarga de observar cuantas iteraciones 
    son necesarias en promedio y como máximo para que el autovector 
    converga por debajo de cierto epsilon.
    El resultado del experimento es de interés ya que nos permite 
    obtener un mayor conocimiento sobre la complejidad del algoritmo.

    Nota: correr el experimento regenera todos los archivos, lo que 
    puede resultar en pequeñas discrepancias con los resultados del 
    informe.
"""


# 
# IO
#

EXPERIMENTO = "op_convergencia"
DIR_IN, DIR_OUT, DIR = IO.createInOut(EXPERIMENTO, delete=True)
RES = f"{DIR}{EXPERIMENTO}.csv"
MATRIZ_IN     = f"{DIR_IN}matriz.txt"
X_IN          = f"{DIR_IN}x.txt"
AVECS_EXPECTED = f"{DIR_IN}avecs_exp.txt"
AVALS_EXPECTED = f"{DIR_IN}avals_exp.txt"

SUMMARY   = f"{DIR}{EXPERIMENTO}_summary.csv"
GRAFICO_MAX = f"{DIR}{EXPERIMENTO}_MAX.png"
GRAFICO_PROM = f"{DIR}{EXPERIMENTO}_PROM.png"

COLS       = 'N,max_iter,prom_iter'
FMT_COLS   = "{0},{1},{2}\n"


#
# VARIABLES
#

N_INICIAL = 2
N_FINAL = 1002 # recomendable que (N_FINAL - N_INICIAL) % STEP = 0
STEP = 100 # tiene que se par para que tenga sentido
EPSILON = 1E-4
TOL = 0
REP = 100


#
# UTILS
#

def make_tests(n):
    print('creando test...')    
    # nos aseguramos de que el autovalor maximo no este repetido
    # para evitar complicaciones que no tienen sentido en este análisis
    S = utils.random_matriz(n, n)
    for i in range(n):
        for j in range(i):
            S[i][j] = S[j][i]

    x = utils.armarRandom(n)

    np.savetxt(MATRIZ_IN, S)
    np.savetxt(X_IN, x)
    return S, x


def pathIter(n):
    return f"{DIR_OUT}t_{n}_iteraciones.out"


#
# RUN 
#

def run_tests():

    for k in range(N_INICIAL, N_FINAL+1, STEP):
        mx = 0
        sum = 0
        print(f'corriendo n: {k}') 
        for j in range(REP):
            S, x = make_tests(k)

            print(f'corriendo REP: {j}') 
            x = np.reshape(x, (k, 1))  
            a = utils.rayleigh(S, x) 
            i = 0

            while(utils.n2(a * x - S @ x) > EPSILON):
                a, x = utils.alt_potencia(S, 2, TOL, x)
                i += 2

            mx = max(mx, i)
            sum += i

        np.savetxt(pathIter(k), [mx, sum/REP])

        
def eval_tests():
    
    print(f'evaluando resultados...') 
    with open(RES, 'a', encoding="utf-8") as file:
        for k in range(N_INICIAL, N_FINAL+1, STEP):
            iteraciones = np.loadtxt(pathIter(k)) 
            file.write(FMT_COLS.format(k, iteraciones[0], iteraciones[1]))


#
# MAIN
#

if __name__ == "__main__":

    run_tests()
    IO.createCSV(RES, COLS)
    eval_tests()

    df = pd.read_csv(RES)
    df.describe().to_csv(SUMMARY)
    
    l = len(df.N)
    utils.graficar(
        x=df.N, 
        y=df.prom_iter, 
        hue=["iteraciones promedio"]*l, 
        xaxis="TAMAÑO DE LA MATRIZ", 
        yaxis="ITERACIONES", 
        filename=GRAFICO_PROM)

    # l = len(df.N)
    # utils.graficar(
    #     x=df.N.to_list() * 2,
    #     y=df.max_iter.to_list() + df.prom_iter.to_list(),
    #     hue=["iteraciones máximas"] * l + ["iteraciones promedio"] * l,
    #     xaxis='TAMAÑO DE LA MATRIZ',
    #     yaxis='ITERACIONES',
    #     filename=GRAFICO_PROM
    # )
