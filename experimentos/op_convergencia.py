import base.IO as IO
import base.utils as utils
from base.utils import n2 as n2

import numpy as np
import pandas as pd


"""
    TODO
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
GRAFICO = f"{DIR}{EXPERIMENTO}.png"

# FMT
COLS       = 'N,iteraciones'
FMT_COLS   = "{0},{1}\n"

# VARIABLES
N = 102 # tiene que terminar en 2
STEP = 10 # tiene que se par para que tenga sentido
TOL = 0
EPSILON = 1E-4
REP = 100


def make_tests(n):
    print('creando test...')    
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
        print(f'corriendo n: {k}') 
        for j in range(REP):
            S, v, x = make_tests(k)

            print(f'corriendo REP: {j}') 
            x = np.reshape(x, (k, 1))  
            v = np.reshape(v, (k, 1))  

            i = 0
            while(True):
                a, x = utils.metodo_potencia(S, 1, TOL, x)
                i += 1
                if(n2(x - v) < EPSILON or n2(x + v) < EPSILON): 
                    break
            mx = max(mx, i)
        np.savetxt(pathIter(k), [mx])

        
        



def pathIter(n):
    return f"{DIR_OUT}t_{n}_iteraciones.out"

def eval_tests():
    
    print(f'evaluando resultados...') 
    with open(RES, 'a', encoding="utf-8") as file:
        for k in range(2, N+1, STEP):
            iteraciones = IO.readAutovalores(pathIter(k)) 
            file.write(FMT_COLS.format(k, iteraciones))


if __name__ == "__main__":

    run_tests()
    IO.createCSV(RES, COLS)
    eval_tests()

    df = pd.read_csv(RES)
    df.describe().to_csv(SUMMARY)
    
    utils.graficar(
        x=df.N, 
        y=df.iteraciones, 
        hue=["caso testigo"]*((N-2)//STEP + 1), 
        xaxis="N", 
        yaxis="ITERACIONES", 
        filename=GRAFICO)
