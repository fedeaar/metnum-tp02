import base.IO as IO
import base.utils as utils

import numpy as np
import pandas as pd

from op_convergencia import EPSILON



"""
    Este experimento se encarga de generar matrices simétricas 
    aleatorias y comprobar que no importa cual sea la lista de 
    autovalores inicial, se cumple que el método de la potencia 
    en conjunto con la deflación funcionan correctamente a la
    hora de calcular la base ortogonal de autovectores y sus 
    correspondientes autovalores.
    Notar que en caso de haber autovalores repetidos la base
    ortogonal de autovectores presenta una infinidad de opciones 
    por lo tanto no se puede comparar por igualdad con los 
    resultados que obtiene numpy.

    Nota: correr el experimento regenera todos los archivos, lo que 
    puede resultar en pequeñas discrepancias con los resultados del 
    informe.
"""


# 
# VARIABLES
#

N = 100
NITER = 20000
TESTS = 100


#
# RUN
#

def run_tests(t):
    S, U, e = utils.armarMatriz([N], N)
    a, V = utils.alt_deflacion(S, N, NITER, 1e-8)

    size = len(a)
    for i in range(N - size): a = np.append(a, 0) #extiendo con 0s

    b = True
    if(utils.n2(V @ V.T) - 1 > EPSILON):
        print("se re pico", utils.n2(V @ V.T))
        b = False

    for v in V.T:
        if(utils.n2(v * (v @ S @ v)  - S @ v) > 1e-3) : # chequeo que sean todos ortogonales
            print(utils.n2(v * (v @ S @ v)  - S @ v))
            b = False

    
    if(b and utils.n2(np.sort(e) - np.sort(a)) < EPSILON): print(str(t)+": Funca")
    else: print(str(t)+": No Funca")


#
# MAIN
#

if __name__ == "__main__":

    for t in range(TESTS):
        run_tests(t)
