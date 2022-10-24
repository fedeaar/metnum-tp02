from distutils.log import error
import base.IO as IO
import base.utils as utils

import numpy as np
import pandas as pd


"""
    TODO
"""


# IO
EXPERIMENTO = "op_mismo_absoluto"
DIR_IN, DIR_OUT, DIR = IO.createInOut(EXPERIMENTO, delete=True)
RES = f"{DIR}{EXPERIMENTO}.csv"
MATRIZ_IN     = f"{DIR_IN}matriz.txt"
X_IN          = f"{DIR_IN}x.txt"
AVECS_EXPECTED = f"{DIR_IN}avecs_exp.txt"
AVALS_EXPECTED = f"{DIR_IN}avals_exp.txt"

# OUT
SUMMARY   = f"{DIR}{EXPERIMENTO}_summary.csv"
GRAFICO_POS = f"{DIR}{EXPERIMENTO}_pos.png"
GRAFICO_NEG = f"{DIR}{EXPERIMENTO}_neg.png"

# FMT
COLS       = 'iter,error_v1,error_v2'
FMT_COLS   = "{0},{1},{2}\n"

# VARIABLES
N = 20
NITER = 100 # tiene que ser par
TOL = 0

def createAutovalores(list, size):
    mn = min(list)
    for i in range(size-len(list)):
        list.append(np.random.randint(abs(mn)-1) + 1)
    return np.array(list)

def make_av_diferentes():
    D = createAutovalores([N, -N], N)    
    D = np.diag(D)
    
    u = np.random.rand(N, 1)
    u = u / utils.norma(u, 2)
    H = np.eye(N) - 2 * (u @ u.T)
    S = H @ D @ H.T

    a, V = utils.eig(S)
    a = a.astype(float)
    V = V.astype(float)
    if(a[0] < a[1]): V.T[[0,1]] = V.T[[1, 0]]


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
    for i in range(NITER+1):
        print(f'corriendo iteracion: {i}') 
        a, x = utils.metodo_potencia(S, 1, TOL, x)
        np.savetxt(pathAvec(i), x)
        np.savetxt(pathAval(i), [a])


def n2(v):
    return np.linalg.norm(v, 2)

def pathAval(i):
    return f"{DIR_OUT}t_{i}_autovalor.out"
    
def pathAvec(i):
    return f"{DIR_OUT}t_{i}_autovector.out"

def cmp(x, y, tol = 1e-3):
    return np.allclose(x, y, tol)

def nml(x):
    return x / n2(x)

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

    vf = IO.readAutovectores(pathAvec( NITER ))
    vantef = IO.readAutovectores(pathAvec( NITER-1 ))

    invertido_r1 = False
    if(cmp(nml(vf + vantef), -q1)): invertido_r1 = True

    invertido_r2 = False
    if(cmp(nml(vf - vantef), -q2)): invertido_r2 = True 

    with open(RES, 'a', encoding="utf-8") as file:
        for i in range(0, NITER, 2):
            print(f'evaluando resultados: {i}') 

            v1 = IO.readAutovectores(pathAvec(i))
            v2 = IO.readAutovectores(pathAvec(i+1))

            r1 = v1 + v2
            r1 = r1 / n2(r1)
            norma2_r1 = n2(r1-q1)
            if invertido_r1: norma2_r1 = 2 - norma2_r1

            r2 = v1 - v2
            r2 = r2 / n2(r2)
            norma2_r2 = n2(r2-q2)
            if invertido_r2: norma2_r2 = 2 - norma2_r2

            file.write(FMT_COLS.format(i, norma2_r1, norma2_r2))

if __name__ == "__main__":

    run_tests()
    IO.createCSV(RES, COLS)
    eval_tests()

    df = pd.read_csv(RES)
    df.describe().to_csv(SUMMARY)
    
    utils.graficar(
        x=df.iter, 
        y=df.error_v1, 
        hue=["caso testigo"]*(NITER//2), 
        xaxis="CANTIDAD DE ITERACIONES", 
        yaxis="ERROR", 
        filename=GRAFICO_POS)
  
    utils.graficar(
        x=df.iter, 
        y=df.error_v2, 
        hue=["caso testigo"]*(NITER//2), 
        xaxis="CANTIDAD DE ITERACIONES", 
        yaxis="ERROR", 
        filename=GRAFICO_NEG)
