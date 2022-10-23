from distutils.log import error
from json.encoder import INFINITY
from os import lstat
from matplotlib.pyplot import step
import base.IO as IO
import base.utils as utils

import numpy as np
import pandas as pd
import itertools


"""
    TODO
"""


# IO
EXPERIMENTO = "mismo_absoluto"
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
COLS       = 'iter,error_autovalor,error_n2_autovectores'
FMT_COLS   = "{0},{1},{2}\n"

# VARIABLES
N = 5
NITER = 20000
STEP = 1000 # tiene que se par para que tenga sentido
TOL = 1e-20

def createAutovalores(list, size):
    list = np.array(list)
    mn = min(list)
    for i in range(size-len(list)):
        list = np.append(list, np.random.randint(abs(mn)))
    return list

def make_av_diferentes():
    D = createAutovalores([N, -N, N, -N], N)    
    D = np.diag(D)
    
    u = np.random.rand(N, 1)
    u = u / utils.norma(u, 2)
    H = np.eye(N) - 2 * (u @ u.T)
    S = H @ D @ H.T

    a, V = utils.eig(S)
    a = a.astype(float)
    V = V.astype(float)
    return S, V, a


def make_tests():
    
    print('creando test...')    
    S, V, a = make_av_diferentes()
    x = np.random.randint(-100, 100, size=(N, N))
    x = x.astype(float)
    x[0] = x[0] / np.linalg.norm(x[0], 2)
    np.savetxt(MATRIZ_IN, S)
    np.savetxt(AVALS_EXPECTED, a)
    np.savetxt(X_IN, x)
    np.savetxt(AVECS_EXPECTED, V)
    return S, x[0]

# RUN 
def run_tests():
    S, x = make_tests()

    print(f'corriendo iteracion: {0}') 
    a, x = utils.metodo_potencia(S, 0, TOL, x)
    np.savetxt(pathAvec(0), x)
    np.savetxt(pathAval(0), [a])

    for i in range(STEP, NITER+1, STEP):
        print(f'corriendo iteracion: {i}') 
        a, x = utils.metodo_potencia(S, STEP, TOL, x)
        np.savetxt(pathAvec(int(i/STEP)), x)
        np.savetxt(pathAval(int(i/STEP)), [a])


def n2(v):
    return np.linalg.norm(v, 2)

def pathAval(i):
    return f"{DIR_OUT}t_{i}_autovalor.out"
def pathAvec(i):
    return f"{DIR_OUT}t_{i}_autovector.out"

def eval_tests():
    # importo S
    S = IO.readMatriz(MATRIZ_IN)

    # importo x
    y0 = IO.readAutovectores(X_IN)
    y0 = y0[0]

    # importo los autovalores esperados
    e = IO.readAutovalores(AVALS_EXPECTED)
    e = e[0]

    # importo los autovectores esperados
    Q = IO.readAutovectores(AVECS_EXPECTED)
    q1 = Q.T[0]
    q2 = Q.T[1]
    vf = IO.readAutovectores(pathAvec( int(NITER/STEP) ))
    
    u = np.dot(y0, q1) * q1 + np.dot(y0, q2) * q2
    u = u / n2(u)
    with open(RES, 'a', encoding="utf-8") as file:
        for i in range(int(NITER/STEP)+1):
            print(f'evaluando resultados: {i}') 

            a = IO.readAutovalores(pathAval(i))
            error = abs(a - e)

            v = IO.readAutovectores(pathAvec(i))
            norma2 = utils.norma(v - u, 2)
            # if invertido: norma2 = 2 - norma2 

            file.write(FMT_COLS.format(i*STEP, error, norma2))

    print("norma2 final:", utils.norma(vf - u, 2))


if __name__ == "__main__":

    run_tests()
    IO.createCSV(RES, COLS)
    eval_tests()

    df = pd.read_csv(RES)
    df.describe().to_csv(SUMMARY)
    
    utils.graficar(
        x=df.iter, 
        # y=df.error_autovalor,
        y=df.error_n2_autovectores, 
        hue=["caso testigo"]*(int(NITER/STEP) + 1), 
        xaxis="CANTIDAD DE ITERACIONES", 
        yaxis="ERROR", 
        filename=GRAFICO)