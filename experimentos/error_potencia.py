import base.IO as IO
import base.utils as utils

import numpy as np
import pandas as pd 
import itertools


"""
    TODO
"""


# IO
EXPERIMENTO = "error-potencia"
DIR_IN, DIR_OUT, DIR = IO.createInOut(EXPERIMENTO)
RES = f"{DIR}{EXPERIMENTO}.csv"

# fmt
COLS       = 'test,tipo,niter,error_n1,error_ninf'
FMT_COLS   = "{0},{1},{2},{3},{4}\n"

# VARIABLES
SEED = 0   # valor semilla
N = 20
MAX_ITER = 25000 #int(1e5)
MAX_VAR  = int(1e4)
MAX_VAR_SDP = 100
STEP = 1000
TESTS = 1
TIPO = ['D', 'H', 'S']


# TESTS 
def make_diagonal(seed=0):
    
    iterator = np.fromiter(itertools.chain(range(MAX_VAR, 0), range(1, MAX_VAR)), int)
    
    np.random.seed(seed)
    diagonal = np.random.choice(iterator, N, replace=False)
    
    return np.diag(diagonal) 


def make_diagonalizable(seed=0):
    
    D = make_diagonal(seed)
    u = np.random.rand(N, 1)
    u = u / utils.norma(u, 2)
    Q = np.eye(N) - 2 * (u @ u.T)
    return  Q @ D @ Q.T


def make_sdp(seed=0):

    np.random.seed(seed)
    S = np.random.randint(-MAX_VAR_SDP, MAX_VAR_SDP, (N, N))
    return S @ S.T


def make_tests():
    
    for i in range(TESTS):
        print(f'creando tests: {i}.')    
        D = make_diagonal(SEED + i*3)
        IO.writeMatriz(D, f"{DIR_IN}t0_{i}.txt")

        H = make_diagonalizable(SEED +i*3 + 1)
        IO.writeMatriz(H, f"{DIR_IN}t1_{i}.txt")
        
        S = make_sdp(SEED + i*3 + 2)
        IO.writeMatriz(S, f"{DIR_IN}t2_{i}.txt")


# RUN 
def run_tests():

    for q in range(STEP, MAX_ITER, STEP):
        for i in range(TESTS):
            print(f'corriendo tests: {i}, q: {q}') 
            for t in range(3):   
                IO.run(f"{DIR_IN}t{t}_{i}.txt", q, 0, o=DIR_OUT, save_as=f"t{t}_{i}_{q}")


def eval_tests():
    
    with open(RES, 'a', encoding="utf-8") as file:
        for q in range(STEP, MAX_ITER, STEP):
            for i in range(TESTS):
                print(f'evaluando resultados: {i}, q: {q}') 
                for t in range(3):
                    M = IO.readMatriz(f"{DIR_IN}t{t}_{i}.txt")
                    a = IO.readAutovalores(f"{DIR_OUT}t{t}_{i}_{q}.autovalores.out")
                    D = np.diag(a)
                    V = IO.readAutovectores(f"{DIR_OUT}t{t}_{i}_{q}.autovectores.out")
                    error = M @ V - V @ D
                    norm1 = np.linalg.norm(error, 1)
                    norminf = np.linalg.norm(error, np.inf)
                    file.write(FMT_COLS.format(i, TIPO[t], q, norm1, norminf))

               


if __name__ == "__main__":

    make_tests()
    run_tests()
    IO.createCSV(RES, COLS)
    eval_tests()

    df = pd.read_csv(RES)
    utils.graficar(
        x=df.niter, 
        y=df.error_n1, 
        hue=df.tipo, 
        xaxis='iteraciones', 
        yaxis='error n1', 
        filename=f"{DIR}n1.png")

    utils.graficar(
        x=df.niter, 
        y=df.error_ninf, 
        hue=df.tipo, 
        xaxis='iteraciones', 
        yaxis='error n1', 
        filename=f"{DIR}ninf.png")
