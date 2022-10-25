import base.IO as IO
import base.utils as utils
from base.utils import n2 as n2

import numpy as np
import pandas as pd


"""
    Este experimento se encarga de observar cuantas iteraciones son necesarias en promedio y como máximo
    para que el autovector converga por debajo de cierto epsilon.
    El resultado del experimento es de interés ya que nos permite obtener un mayor conocimiento sobre la complejidad del algoritmo
"""


# IO
EXPERIMENTO = "op_convergencia"
DIR_IN, DIR_OUT, DIR = IO.createInOut(EXPERIMENTO, delete=True)
RES = f"{DIR}{EXPERIMENTO}.csv"
MATRIZ_IN     = f"{DIR_IN}matriz.txt"
X_IN          = f"{DIR_IN}x.txt"
AVECS_EXPECTED = f"{DIR_IN}avecs_exp.txt"
AVALS_EXPECTED = f"{DIR_IN}avals_exp.txt"

# OUT
SUMMARY   = f"{DIR}{EXPERIMENTO}_summary.csv"
GRAFICO_MAX = f"{DIR}{EXPERIMENTO}_MAX.png"
GRAFICO_PROM = f"{DIR}{EXPERIMENTO}_PROM.png"

# FMT
COLS       = 'N,max_iter,prom_iter'
FMT_COLS   = "{0},{1},{2}\n"

# VARIABLES
N = 102 # tiene que terminar en 2
STEP = 10 # tiene que se par para que tenga sentido
TOL = 0
EPSILON = 1E-4
REP = 10


def make_tests(n):
    print('creando test...')    
    # nos aseguramos de que el autovalor maximo no este repetido
    # para evitar complicaciones que no tienen sentido en este análisis
    S, V, a = utils.armarMatriz([n], n) 
    x = utils.armarRandom(n)

    np.savetxt(MATRIZ_IN, S)
    np.savetxt(AVALS_EXPECTED, a)
    np.savetxt(X_IN, x)
    np.savetxt(AVECS_EXPECTED, V)
    return S, V.T[0], x

# RUN 
def run_tests():

    for k in range(2, N+1, STEP):
        mx = 0
        sum = 0
        print(f'corriendo n: {k}') 
        for j in range(REP):
            S, v, x = make_tests(k)

            print(f'corriendo REP: {j}') 
            x = np.reshape(x, (k, 1))  
            v = np.reshape(v, (k, 1))  

            i = 0
            while(True):
                a, x = utils.alt_potencia(S, 2, TOL, x)
                i += 2
                if(n2(x - v) < EPSILON or n2(x + v) < EPSILON): 
                    break
            mx = max(mx, i)
            sum += i

        np.savetxt(pathIter(k), [mx, sum/REP])

        
        
def pathIter(n):
    return f"{DIR_OUT}t_{n}_iteraciones.out"

def eval_tests():
    
    print(f'evaluando resultados...') 
    with open(RES, 'a', encoding="utf-8") as file:
        for k in range(2, N+1, STEP):
            iteraciones = IO.readAutovalores(pathIter(k)) 
            file.write(FMT_COLS.format(k, iteraciones[0], iteraciones[1]))


if __name__ == "__main__":

    run_tests()
    IO.createCSV(RES, COLS)
    eval_tests()

    df = pd.read_csv(RES)
    df.describe().to_csv(SUMMARY)
    
    utils.graficar(
        x=df.N, 
        y=df.max_iter, 
        hue=["iteraciones máximas"]*((N-2)//STEP + 1), 
        xaxis="TAMAÑO DE LA MATRIZ", 
        yaxis="ITERACIONES", 

        filename=GRAFICO_MAX)

    utils.graficar(
        x=df.N, 
        y=df.prom_iter, 
        hue=["iteraciones promedio"]*((N-2)//STEP + 1), 
        xaxis="TAMAÑO DE LA MATRIZ", 
        yaxis="ITERACIONES", 
        filename=GRAFICO_PROM)
