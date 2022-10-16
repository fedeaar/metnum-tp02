import base.IO as IO
import base.utils as utils

import numpy as np
import itertools

"""
    casos de TEST para ./tp2 generados de manera aleatoria (con un valor semilla).

    Cada test satisface que la matriz asociada (n x n) tiene n autovalores reales
    diferentes en magnitud (descontando multiplicidad).
"""


# GLOBALS
TEST_DIR = "./tests-generados"

S = 0   # valor semilla


# UTILS
def assert_results(M, w, V):

    test = np.allclose(M @ V,  V @ np.diag(w), utils.EPSILON, utils.EPSILON)
    assert(test)


def make_test(M, niter, tol, w, filename):

    IO.writeAutovalores(niter, tol, w, f"{TEST_DIR}/{filename}.autovalores.out")
    IO.writeMatriz(M, f"{TEST_DIR}/{filename}.txt")
    

# TESTS 
def TESTS_diagonales(n=10, t=10, niter=10000, tol=1e-20, seed=None):
    
    for i in range(t):
        if seed:
            np.random.seed(seed + i)
        iterator = np.fromiter(itertools.chain(range(int(-1e4), 0), range(1, int(1e4))), int)
        diagonal = np.random.choice(iterator, n, replace=False)
        D = np.diag(diagonal)

        w, V = utils.eig(D) # utils.metodo_deflacion(D, n, niter, tol)
        
        assert_results(D, w, V)
        make_test(D, niter, tol, w, "diagonal_" + str(i + 1))
        

def TESTS_householder(n=10, t=10, niter=10000, tol=1e-20, seed=None):
    
    for i in range(t):
        if seed:
            np.random.seed(seed + i)
        iterator = np.fromiter(itertools.chain(range(int(-1e4), 0), range(1, int(1e4))), int)
        diagonal = np.random.choice(iterator, n, replace=False)
        D = np.diag(diagonal)
        u = np.random.rand(n, 1)
        u = u / utils.norma(u, 2)
        Q = np.eye(n) - 2 * (u @ u.T)
        M = Q @ D @ Q.T

        w, V = utils.eig(M) #metodo_deflacion(M, n, niter, tol)
   
        assert_results(M, w, V)
        make_test(M, niter, tol, w, "householder_" + str(i + 1))


def TESTS_sdp(n=10, t=10, niter=10000, tol=1e-15, seed=None):
    
    for i in range(t):
        if seed:
            np.random.seed(seed + i)
        S = np.random.randint(1, 100, (n, n))
        S = S @ S.T

        w, V = utils.eig(S) #metodo_deflacion(S, n, niter, tol)
   
        assert_results(S, w, V)
        make_test(S, niter, tol, w, "sdp_" + str(i + 1))


def TESTS_especiales(niter=10000, tol=1e-10):

    # simetrico
    n = 3
    A = np.array([
        [ 7,  2,  -3],
        [ 2,  2,  -2],
        [-3, -2,  -2]
    ])
    w, V = utils.eig(A) #metodo_deflacion(A, n, niter, tol)
    
    assert_results(A, w, V)
    make_test(A, niter, tol, w, "simetrico")





if __name__ == "__main__":
    
    TESTS_diagonales(seed=S)
    TESTS_householder(seed=S+10)
    TESTS_sdp(seed=S+20)
    TESTS_especiales()
