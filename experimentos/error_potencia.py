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
DIR_IN, DIR_OUT, DIR = IO.createInOut(EXPERIMENTO, delete=True)
RES = f"{DIR}{EXPERIMENTO}.csv"

# OUT
SUMMARY   = f"{DIR}{EXPERIMENTO}_summary.csv"
SUMMARY_D = f"{DIR}{EXPERIMENTO}_summary_d.csv"
SUMMARY_H = f"{DIR}{EXPERIMENTO}_summary_h.csv"
SUMMARY_S = f"{DIR}{EXPERIMENTO}_summary_s.csv"

# FMT
COLS       = 'test,tipo,error_n1_rel,error_ninf_rel,error_n1_abs,error_ninf_abs,min_aval,max_aval'
FMT_COLS   = "{0},{1},{2},{3},{4},{5},{6},{7}\n"

# VARIABLES
SEED = 0 # valor semilla
N = 20
MAX_VAR  = int(1e3) # par
MAX_VAR_SDP = int(1e3)
TESTS = 100
TIPO = ['D', 'H', 'S']
NITER = 20000
TOL = 1e-20

# TESTS 
def make_diagonal(seed=0):
    
    iterator = np.fromiter(itertools.chain(range(-MAX_VAR, 0, 2), range(1, MAX_VAR, 2)), int)
    
    np.random.seed(seed)
    diagonal = np.random.choice(iterator, N, replace=False)
    
    idx = np.argsort(np.abs(diagonal))[::-1]
    return  diagonal[idx], np.diag(diagonal) 


def make_diagonalizable(seed=0):
    
    a, D = make_diagonal(seed)
    np.random.seed(seed)
    u = np.random.rand(N, 1)
    u = u / np.linalg.norm(u, 2)
    Q = np.eye(N) - 2 * (u @ u.T)
    return  a, Q @ D @ Q.T


def make_sdp(seed=0):

    np.random.seed(seed)
    S = np.random.randint(-MAX_VAR_SDP, MAX_VAR_SDP, (N, N))
    S = S @ S.T
    a, V = np.linalg.eig(S)
    idx = np.argsort(np.abs(a))[::-1]
    return a[idx], S


def make_tests():
    
    for i in range(TESTS):
        print(f'creando tests: {i}.')    
        a, D = make_diagonal(SEED + i*3)
        IO.writeMatriz(D, f"{DIR_IN}t0_{i}.txt")
        IO.writeMatriz(a, f"{DIR_IN}t0_{i}_expected.txt")

        a, H = make_diagonalizable(SEED +i*3 + 1)
        IO.writeMatriz(H, f"{DIR_IN}t1_{i}.txt")
        IO.writeMatriz(a, f"{DIR_IN}t1_{i}_expected.txt")

        a, S = make_sdp(SEED + i*3 + 2)
        IO.writeMatriz(S, f"{DIR_IN}t2_{i}.txt")
        IO.writeMatriz(a, f"{DIR_IN}t2_{i}_expected.txt")

# RUN 
def run_tests():

    for i in range(TESTS):
        print(f'corriendo tests: {i}') 
        for t in range(3):   
            IO.run(f"{DIR_IN}t{t}_{i}.txt", NITER, TOL, o=DIR_OUT, save_as=f"t{t}_{i}")


def eval_tests():
    
    with open(RES, 'a', encoding="utf-8") as file:
        for i in range(TESTS):
            print(f'evaluando resultados: {i}') 
            for t in range(3):
                M = IO.readMatriz(f"{DIR_IN}t{t}_{i}.txt")
                a = IO.readAutovalores(f"{DIR_OUT}t{t}_{i}.autovalores.out")
                e = IO.readAutovalores(f"{DIR_IN}t{t}_{i}_expected.txt")
                D = np.diag(a)
                V = IO.readAutovectores(f"{DIR_OUT}t{t}_{i}.autovectores.out")

                error_rel = M @ V - V @ D
                error_abs = a - e
                norm1_rel = np.linalg.norm(error_rel, 1)
                norminf_rel = np.linalg.norm(error_rel, np.inf)
                norm1_abs = np.linalg.norm(error_abs, 1)
                norminf_abs = np.linalg.norm(error_abs, np.inf)

                file.write(FMT_COLS.format(i, TIPO[t], norm1_rel, norminf_rel, norm1_abs, norminf_abs, np.min(a), np.max(a)))

               


if __name__ == "__main__":

    make_tests()
    run_tests()
    IO.createCSV(RES, COLS)
    eval_tests()

    df = pd.read_csv(RES)
    df.describe().to_csv(SUMMARY)
    df.query("tipo=='D'").describe().to_csv(SUMMARY_D)
    df.query("tipo=='H'").describe().to_csv(SUMMARY_H)
    df.query("tipo=='S'").describe().to_csv(SUMMARY_S)
