import numpy as np
import base.IO as IO
import base.utils as utils


"""
    casos de TEST para ./tp2 generados de manera aleatoria 
    (con un valor semilla)

    Cada test satisface que la matriz asociada (n x n) tiene n 
    autovalores positivos diferentes.

"""

# GLOBALS
TEST_DIR = "../tests"


# UTILS
def assert_results(M, w, V):

    assert(len(w) == len(np.unique(w)))
    test = np.allclose(M @ V,  V @ np.diag(w), utils.EPSILON, utils.EPSILON)
    assert(test)


def make_test(M, niter, tol, w, filename):

    IO.writeAutovalores(niter, tol, w, f"{TEST_DIR}/{filename}.autovalores.out")
    IO.writeMatriz(M, f"{TEST_DIR}/{filename}.txt")
    

# TESTS 
def TESTS_diagonales(n=10, t=10, niter=10000, tol=1e-10, seed=None):
    
    for i in range(t):
        if seed:
            np.random.seed(seed + i)
        diagonal = np.random.choice([x if i % 2 == 0 else -x for i, x in enumerate(range(1, 100))], n, replace=False)
        D = np.diag(diagonal)

        w, V = utils.metodo_deflacion(D, n, niter, tol)
        
        assert_results(D, w, V)
        make_test(D, niter, tol, w, "diagonal_" + str(i + 1))
        

def TESTS_householder(n=10, t=10, niter=10000, tol=1e-10, seed=None):
    
    for i in range(t):
        if seed:
            np.random.seed(seed + i)
        diagonal = np.random.choice([x if i % 2 == 0 else -x for i, x in enumerate(range(1, 100))], n, replace=False)
        D = np.diag(diagonal)
        u = np.random.rand(n, 1)
        u = u / utils.norma(u, 2)
        Q = np.eye(n) - 2 * (u @ u.T)
        M = Q @ D @ Q.T

        w, V = utils.metodo_deflacion(M, n, niter, tol)
   
        assert_results(M, w, V)
        make_test(M, niter, tol, w, "householder_" + str(i + 1))


def TESTS_sdp(n=10, t=10, niter=10000, tol=1e-10, seed=None):
    
    for i in range(t):
        if seed:
            np.random.seed(seed + i)
        S = np.random.randint(1, 100, (n, n))
        S = S @ S.T

        w, V = utils.metodo_deflacion(S, n, niter, tol)
   
        assert_results(S, w, V)
        make_test(S, niter, tol, w, "sdp_" + str(i + 1))


def TESTS_especiales(niter=20000, tol=1e-24):

    n = 3

    # simetrico
    A = np.array([
        [ 7,  2,  -3],
        [ 2,  2,  -2],
        [-3, -2,  -2]
    ])
    w, V = utils.metodo_deflacion(A, n, niter, tol)
    
    assert_results(A, w, V)
    make_test(A, niter, tol, w, "simetrico")

    
    # error numerico
    A = np.array([
        [7, 2, 3],
        [0, 2, 0],
        [-6, -2, -2]
    ])
    w, V = utils.eig(A) # utils.metodo_deflacion(A, n, niter, tol)

    assert_results(A, w, V)

    w = np.sort(w)[::-1]
    make_test(A, niter, tol, w, "error_num")




if __name__ == "__main__":

    s = 0
    TESTS_diagonales(seed=s)
    TESTS_householder(seed=s+10)
    TESTS_sdp(seed=s+20)
    TESTS_especiales()
