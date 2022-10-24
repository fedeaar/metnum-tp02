import base.IO as IO
import base.utils as utils

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
NITER = 200
N = 202
STEP = 10 # tiene que se par para que tenga sentido
TOL = 0
EPSILON = 1E-4
REP = 10

def createAutovalores(list, size):
    list = np.array(list)
    mn = min(list)
    for i in range(size-len(list)):
        list = np.append(list, np.random.randint(abs(mn)))
    return list

def expected(n):
    D = createAutovalores([n], n)    
    D = np.diag(D)
    
    u = np.random.rand(n, 1)
    u = u / utils.norma(u, 2)
    H = np.eye(n) - 2 * (u @ u.T)
    S = H @ D @ H.T

    a, V = utils.eig(S)
    a = a.astype(float)
    V = V.astype(float)
    return S, V, a


def make_tests(n):
    print('creando test...')    
    S, V, a = expected(n)
    x = np.random.randint(-100, 100, size=(n, n))
    x = x.astype(float)
    x[0] = x[0] / np.linalg.norm(x[0], 2)
    np.savetxt(MATRIZ_IN, S)
    np.savetxt(AVALS_EXPECTED, a)
    np.savetxt(X_IN, x)
    np.savetxt(AVECS_EXPECTED, V)
    return S, V.T[0], a[0], x[0]

# RUN 
def run_tests():

    for k in range(2, N+1, STEP):
        sum = 0
        print(f'corriendo n: {k}') 
        for j in range(REP):
            print(f'corriendo REP: {j}') 
            
            S, v, e, x = make_tests(k)  
            i = 0
            while(True):
                a, x = utils.metodo_potencia(S, 1, TOL, x)
                i += 1
                if(n2(x - v) < EPSILON or n2(x + v) < EPSILON): 
                    break
            sum += i
        np.savetxt(pathIter(k), [sum/REP])

        
        


def n2(v):
    return np.linalg.norm(v, 2)

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
        hue=["caso testigo"]*(int((N-2)/STEP) + 1), 
        xaxis="N", 
        yaxis="ITERACIONES", 
        filename=GRAFICO)
