from distutils.log import error
import base.IO as IO
import base.utils as utils

import numpy as np
import pandas as pd



"""
    TODO
"""


# IO
EXPERIMENTO = "op_autovalor_repetido_bis"
DIR_IN, DIR_OUT, DIR = IO.createInOut(EXPERIMENTO, delete=True)
RES = f"{DIR}{EXPERIMENTO}.csv"
MATRIZ_IN     = f"{DIR_IN}matriz.txt"
X_IN          = f"{DIR_IN}x.txt"
AVECS_EXPECTED = f"{DIR_IN}avecs_exp.txt"
AVALS_EXPECTED = f"{DIR_IN}avals_exp.txt"

# OUT
SUMMARY   = f"{DIR}{EXPERIMENTO}_summary.csv"
GRAFICO_AVAL = f"{DIR}{EXPERIMENTO}_val.png"
GRAFICO_AVEC = f"{DIR}{EXPERIMENTO}_vec.png"

# FMT
COLS       = 'iter,error_autovalor,error_n2_autovectores'
FMT_COLS   = "{0},{1},{2}\n"

# VARIABLES
N = 20
NITER = 1000
STEP = 1 # tiene que se par para que tenga sentido
TOL = 0

def createAutovalores(list, size):
    mn = min(list)
    for i in range(size-len(list)):
        list.append(np.random.randint(abs(mn)-1) + 1)
    return np.array(list)

def make_av_diferentes():
    D = createAutovalores([N], N)   
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
    return S, V, a,  x[0]

# RUN 
def run_tests():
    S, V, e, x = make_tests()

    a, U = utils.metodo_deflacion(S, N)

    b = True
    for i in range(N):
        for j in range(i+1, N):
            if(abs(np.inner(U.T[i], U.T[j])) > utils.EPSILON) :
                print(abs(np.inner(U.T[i], U.T[j])))
                b = False

    for i in range(N):
        if(abs(np.inner(U.T[i], U.T[i]) - 1) > utils.EPSILON) :
            b = False

    if(b and np.allclose(a, e)): print("Funca")
    else: print("No Funca")


def n2(v):
    return np.linalg.norm(v, 2)

def pathAval(i):
    return f"{DIR_OUT}t_{i}_autovalor.out"
def pathAvec(i):
    return f"{DIR_OUT}t_{i}_autovector.out"

def eval_tests():
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

            file.write(FMT_COLS.format(i*STEP, error, norma2))
    print(vf.T @ S @ vf)

if __name__ == "__main__":
    run_tests()