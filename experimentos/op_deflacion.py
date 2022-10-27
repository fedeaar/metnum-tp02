from cmath import inf
import base.IO as IO
import base.utils as utils

import numpy as np
import pandas as pd

from op_convergencia import EPSILON



"""
    Este experimento se encarga de generar matrices simétricas aleatorias y comprobar que 
    no importa cual sea la lista de autovalores inicial, se cumple que el método de la potencia 
    en conjunto con la deflación funcionan correctamente a la hora de calcular la base ortogonal
    de autovectores y sus correspondientes autovalores.
    Notar que en caso de haber autovalores repetidos la base ortogonal de autovectores presenta una 
    infinidad de opciones por lo tanto no se puede comparar por igualdad con los resultados que obtiene numpy.
"""



# VARIABLES
N = 100
NITER = 20000

def run_tests():
    S, U, e = utils.armarMatriz([N], N)
    a, V = utils.alt_deflacion(S, N, NITER, 1e-8)

    size = len(a)
    b = True
    for i in range(size):
        for j in range(i+1, size):
            if(abs(np.inner(V.T[i], V.T[j])) > 1e-3) : # chequeo que sean todos ortogonales
                print(abs(np.inner(V.T[i], V.T[j])))
                b = False

    for v in V.T:
        if(utils.n2(v * (v @ S @ v)  - S @ v) > 1e-3) : # chequeo que sean todos ortogonales
            print(utils.n2(v * (v @ S @ v)  - S @ v))
            b = False

    a = np.pad(a, N - size) # extiendo a agregandole 0s las veces que corresponda con su multiplicidad
    
    if(b and utils.n2(np.sort(e) - np.sort(a)) < EPSILON): print("Funca")
    else: print("No Funca")


if __name__ == "__main__":
    run_tests()