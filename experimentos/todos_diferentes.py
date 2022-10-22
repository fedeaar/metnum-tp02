from distutils.log import error
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
EXPERIMENTO = "todos_diferentes"
DIR_IN, DIR_OUT, DIR = IO.createInOut(EXPERIMENTO, delete=True)
RES = f"{DIR}{EXPERIMENTO}.csv"

# OUT
SUMMARY   = f"{DIR}{EXPERIMENTO}_summary.csv"
GRAFICO = f"{DIR}{EXPERIMENTO}.png"

# FMT
COLS       = 'iter,error_autovalor,error_n2_autovectores'
FMT_COLS   = "{0},{1},{2}\n"

# VARIABLES
N = 20
NITER = 1000
STEP = 100 # tiene que se par para que tenga sentido
TOL = 1e-20

def createAutovalores(list, size):
    mn = min(list)
    for i in range(size-len(list)):
        list.append(np.random.randint(abs(mn)))
    return list

def make_av_diferentes():
    D = createAutovalores([N], N)
    print(D)
    D = np.diag(D)

    u = np.random.rand(N, 1)
    u = u / utils.norma(u, 2)
    H = np.eye(N) - 2 * (u @ u.T)
    S = H @ D @ H.T

    a, V = utils.eig(S)
    return S, V, a


def make_tests():
    
    print('creando test...')    
    S, V, a = make_av_diferentes()
    x = np.random.randint(-100, 100, size=(N, N))
    x = x.astype(float)
    x[0] = x[0] / np.linalg.norm(x[0], 2)
    np.savetxt(f"{DIR_IN}t_matriz.txt", S)
    np.savetxt(f"{DIR_IN}t_autovalores_dom.txt", a)
    np.savetxt(f"{DIR_IN}t0_x.txt", x)
    np.savetxt(f"{DIR_IN}t_autovectores_dom.txt", V)


# RUN 
def run_tests():
    print(f'corriendo iteracion: {0}') 
    IO.run(f"{DIR_IN}t_matriz.txt", 0, TOL, x=f"{DIR_IN}t0_x.txt", o=DIR_OUT, save_as=f"t_{0}")
    for i in range(STEP, NITER, STEP):
        print(f'corriendo iteracion: {i}') 
        IO.run(f"{DIR_IN}t_matriz.txt", 1, TOL, x=f"{DIR_OUT}t_{int(i/STEP)-1}.autovectores.out", o=DIR_OUT, save_as=f"t_{int(i/STEP)}")

def n2(v):
    return np.linalg.norm(v, 2)

def eval_tests():
    
    with open(RES, 'a', encoding="utf-8") as file:
        for i in range(int(NITER/STEP)):
            print(f'evaluando resultados: {i}') 

            a = IO.readAutovalores(f"{DIR_OUT}t_{i}.autovalores.out")
            a_d = a[0]
            e = IO.readAutovalores(f"{DIR_IN}t_autovalores_dom.txt")
            e_d = e[0]
            error = abs(a_d - e_d)

            V = IO.readAutovectores(f"{DIR_OUT}t_{i}.autovectores.out")
            v_d = V[0]
            Q = IO.readAutovectores(f"{DIR_IN}t_autovectores_dom.txt")
            q_d = Q.T[0]
            # if(n2(q_d) > 0 and n2(v_d) < 0): v_d = -1 * v_d

            norma2 = np.linalg.norm(v_d - q_d, 2)

            file.write(FMT_COLS.format(i*STEP, error, norma2))


if __name__ == "__main__":

    make_tests()
    run_tests()
    IO.createCSV(RES, COLS)
    eval_tests()

    df = pd.read_csv(RES)
    df.describe().to_csv(SUMMARY)
    
    utils.graficar(
        x=df.iter, 
        y=df.error_autovalor,
        # y=df.error_n2_autovectores, 
        hue=["caso testigo"]*(int(NITER/STEP)), 
        xaxis="CANTIDAD DE ITERACIONES", 
        yaxis="ERROR", 
        filename=GRAFICO)