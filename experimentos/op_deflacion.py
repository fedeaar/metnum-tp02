import base.IO as IO
import base.utils as utils

import numpy as np
import pandas as pd



"""
    TODO
"""



# VARIABLES
N = 20
NITER = 1000
TOL = 0


def run_tests():
    S, V, e = utils.armarMatriz([N,N], N)

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


if __name__ == "__main__":
    run_tests()