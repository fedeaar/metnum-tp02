import base.IO as IO

import numpy as np
import pandas as pd
import itertools


"""
descripcion: 
    evaluación del metodo de la potencia para un subconjunto pequeño
    de matrices. 

    Nota: correr el experimento regenera todos los archivos, lo que 
    puede resultar en pequeñas discrepancias con los resultados del 
    informe.
"""


# 
# OUT
#

EXPERIMENTO = "error-potencia"
DIR_IN, DIR_OUT, DIR = IO.createInOut(EXPERIMENTO, delete=True)

RES = f"{DIR}{EXPERIMENTO}.csv"

SUMMARY   = f"{DIR}{EXPERIMENTO}_summary.csv"
SUMMARY_D = f"{DIR}{EXPERIMENTO}_summary_d.csv"
SUMMARY_H = f"{DIR}{EXPERIMENTO}_summary_h.csv"
SUMMARY_S = f"{DIR}{EXPERIMENTO}_summary_s.csv"

COLS       = 'test,tipo,error_n1_rel,error_ninf_rel,error_n1_abs,error_ninf_abs,min_aval,max_aval'
FMT_COLS   = "{0},{1},{2},{3},{4},{5},{6},{7}\n"


# 
# VARIABLES
#

SEED        = 0
N           = 20
TESTS       = 100
NITER       = 20000
TOL         = 1e-20
MAX_VAR     = int(1e3)          # autovalores
MAX_VAR_SDP = int(1e3)          # elementos de la matriz
TIPO        = ['D', 'H', 'S']


# 
# UTILS 
#

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
        np.savetxt(DIR_IN + f"t0_{i}.txt", D)
        np.savetxt(DIR_IN + f"t0_{i}_expected.txt", a)

        a, H = make_diagonalizable(SEED +i*3 + 1)
        np.savetxt(DIR_IN + f"t1_{i}.txt", H)
        np.savetxt(DIR_IN + f"t1_{i}_expected.txt", a)

        a, S = make_sdp(SEED + i*3 + 2)
        np.savetxt(DIR_IN + f"t2_{i}.txt", S)
        np.savetxt(DIR_IN + f"t2_{i}_expected.txt", a)


# 
# EXPERIMENTO 
#

def run_tests():

    for i in range(TESTS):
        print(f'corriendo tests: {i}') 
        for t in range(3):   
            IO.run(DIR_IN + f"t{t}_{i}.txt", NITER, TOL, o=DIR_OUT)


def eval_tests():
    
    IO.createCSV(RES, COLS)
    with open(RES, 'a', encoding="utf-8") as file:
        for i in range(TESTS):
            print(f'evaluando resultados: {i}') 
            for t in range(3):
                M = np.loadtxt(DIR_IN + f"t{t}_{i}.txt")
                a = np.loadtxt(DIR_OUT + f"t{t}_{i}.autovalores.out")
                e = np.loadtxt(DIR_IN + f"t{t}_{i}_expected.txt")
                D = np.diag(a)
                V = np.loadtxt(DIR_OUT + f"t{t}_{i}.autovectores.out")

                error_rel = M @ V - V @ D
                error_abs = a - e
                norm1_rel = np.linalg.norm(error_rel, 1)
                norminf_rel = np.linalg.norm(error_rel, np.inf)
                norm1_abs = np.linalg.norm(error_abs, 1)
                norminf_abs = np.linalg.norm(error_abs, np.inf)

                line = FMT_COLS.format(i, TIPO[t], norm1_rel, norminf_rel, norm1_abs, norminf_abs, np.min(a), np.max(a))
                file.write(line)


#
# MAIN
# 

if __name__ == "__main__":

    make_tests()
    run_tests()
    eval_tests()

    df = pd.read_csv(RES)
    df.describe().to_csv(SUMMARY)
    df.query("tipo=='D'").describe().to_csv(SUMMARY_D)
    df.query("tipo=='H'").describe().to_csv(SUMMARY_H)
    df.query("tipo=='S'").describe().to_csv(SUMMARY_S)
