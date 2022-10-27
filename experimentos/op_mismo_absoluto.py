import base.IO as IO
import base.utils as utils
from base.utils import n2 as n2
from base.utils import nml as nml

import numpy as np
import pandas as pd


"""
    Este experimento se encarga de observar si el método de 
    la potencia converge y a que autovalor converge en caso de que 
    el autovalor dominante de la matriz este repetido pero en módulo.
    
    A diferencia del experimento "op_autovalor_repetido" aquí si 
    tiene sentido chequear con numpy a que autovectores converge 
    el método ya que las opciones estan limitadas por lo explicado 
    en el informe.

    Nota: correr el experimento regenera todos los archivos, lo que 
    puede resultar en pequeñas discrepancias con los resultados del 
    informe.
"""


# 
# IO
#

EXPERIMENTO = "op_mismo_absoluto"
DIR_IN, DIR_OUT, DIR = IO.createInOut(EXPERIMENTO, delete=True)
RES = f"{DIR}{EXPERIMENTO}.csv"
MATRIZ_IN     = f"{DIR_IN}matriz.txt"
X_IN          = f"{DIR_IN}x.txt"
AVECS_EXPECTED = f"{DIR_IN}avecs_exp.txt"
AVALS_EXPECTED = f"{DIR_IN}avals_exp.txt"

SUMMARY   = f"{DIR}{EXPERIMENTO}_summary.csv"
GRAFICO_POS = f"{DIR}{EXPERIMENTO}_pos.png"
GRAFICO_NEG = f"{DIR}{EXPERIMENTO}_neg.png"
GRAFICO_OSC = f"{DIR}{EXPERIMENTO}_osc.png"

COLS       = 'iter,error_v1,error_v2'
FMT_COLS   = "{0},{1},{2}\n"

# 
# VARIABLES
#

N = 20
NITER = 100 # tiene que ser par
TOL = 0


#
# UTILS
#

def make_tests():
    
    print('creando test...')    
    # nos aseguramos que haya 2 autovalores dominantes iguales en módulo
    S, V, a = utils.armarMatriz([-N, N], N) 
    x = utils.armarRandom(N)
    np.savetxt(MATRIZ_IN, S)
    np.savetxt(AVALS_EXPECTED, a)
    np.savetxt(X_IN, x)
    np.savetxt(AVECS_EXPECTED, V)
    return S, x


def pathAval(i):
    return f"{DIR_OUT}t_{i}_autovalor.out"
    

def pathAvec(i):
    return f"{DIR_OUT}t_{i}_autovector.out"


def cmp(x, y, tol=1e-4):
    return np.allclose(x, y, tol)


# 
# RUN 
#

def run_tests():
    S, x = make_tests()
    print(f'corriendo iteracion: 0') 
    a, x = utils.metodo_potencia(S, 0, TOL, np.reshape(x, (N, 1)))
    np.savetxt(pathAvec(0), x)
    np.savetxt(pathAval(0), [a])
    for i in range(1, NITER+1):
        print(f'corriendo iteracion: {i}') 
        a, x = utils.metodo_potencia(S, 1, TOL, np.reshape(x, (N, 1)))
        np.savetxt(pathAvec(i), x)
        np.savetxt(pathAval(i), [a])




def eval_tests():
    # importo S
    S = np.loadtxt(MATRIZ_IN)

    # importo x
    y0 = np.loadtxt(X_IN)

    # importo los autovalores esperados
    e = np.loadtxt(AVALS_EXPECTED)
    e = e[0]

    # importo los autovectores esperados
    Q = np.loadtxt(AVECS_EXPECTED)
    q1 = Q.T[0]
    q2 = Q.T[1]

    # elijo un vector aleatorio constante que sirva de referencia
    u = np.random.rand(N, 1)
    u = nml(u)

    vf = np.loadtxt(pathAvec( NITER ))
    vantef = np.loadtxt(pathAvec( NITER-1 ))

    invertido_r1 = False
    if(cmp(nml(vf + vantef), -q1, 0.2)): 
        invertido_r1 = True

    invertido_r2 = False
    if(cmp(nml(vf - vantef), -q2, 0.2)): 
        invertido_r2 = True 

    osclist = []
    with open(RES, 'a', encoding="utf-8") as file:
        for i in range(0, NITER, 2):
            print(f'evaluando resultados: {i}') 

            v1 = np.loadtxt(pathAvec(i))
            v2 = np.loadtxt(pathAvec(i+1))

            r1 = v1 + v2
            r1 = r1 / n2(r1)
            norma2_r1 = n2(r1-q1)
            if invertido_r1: norma2_r1 = 2 - norma2_r1

            r2 = v1 - v2
            r2 = r2 / n2(r2)
            norma2_r2 = n2(r2-q2)
            if invertido_r2: norma2_r2 = 2 - norma2_r2

            # almaceno la distancia del vector de la iteracion i con el aleatorio constante de referencia
            osclist.append(n2(v1 - u))
            
            # almaceno la distancia del vector de la iteracion i+1 con el aleatorio constante de referencia
            osclist.append(n2(v2 - u))

            file.write(FMT_COLS.format(i, norma2_r1, norma2_r2))

    utils.graficar(
        x=np.arange(NITER, dtype=int), 
        y=osclist, 
        hue=["caso testigo"]*(NITER), 
        xaxis="cantidad de iteraciones", 
        yaxis="distancia al vector aleatorio", 
        filename=GRAFICO_OSC)




#
# MAIN
#

if __name__ == "__main__":

    run_tests()
    IO.createCSV(RES, COLS)
    eval_tests()

    df = pd.read_csv(RES)
    df.describe().to_csv(SUMMARY)
    
    utils.graficar(
        x=df.iter, 
        y=df.error_v1, 
        hue=["convergencia del autovector cuyo autovalor es positivo"]*(NITER//2), 
        xaxis="CANTIDAD DE ITERACIONES", 
        yaxis="ERROR", 
        filename=GRAFICO_POS)
  
    utils.graficar(
        x=df.iter, 
        y=df.error_v2, 
        hue=["convergencia del autovector cuyo autovalor es negativo"]*(NITER//2), 
        xaxis="CANTIDAD DE ITERACIONES", 
        yaxis="ERROR", 
        filename=GRAFICO_NEG)
