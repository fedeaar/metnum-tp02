from tkinter import E
import base.IO as IO
import base.utils as utils

import numpy as np
import pandas as pd

from error_potencia import TOL


"""
descripcion:
"""

# IO
EXPERIMENTO          = "todos_con_todos"
DIR_IN, DIR_OUT, DIR = IO.createInOut(EXPERIMENTO)    
RESULTADOS           = f"{DIR}{EXPERIMENTO}.csv"
SUMMARY              = f"{DIR}{EXPERIMENTO}_summary.csv"
GRAFICO              = f"{DIR}{EXPERIMENTO}.png"

# fmt
COLS       = 'tol,,q_nodos'
FMT_COLS   = "{0},{1},{2}\n"

# variables
N = 10000   # cantidad total de iteraciones
TOL = 1e-10  # valor p

def correrMetodoPotenciaCpp(out_dir, A, niter, tol):
    return 

# metodos
def correr_potencia():
    A = np.diag([5, -5, 2, 1, 0])
    for i in range(1, N + 1):        
        caso = DIR_IN + "c"+ str(i) + ".txt"
        IO.createFileIn(caso, A)
        correrMetodoPotenciaCpp(DIR_OUT, A, i, TOL)


def medir():

    with open(RESULTADOS, "a", encoding="utf-8") as file:

        for i in range(1, N+1):

            caso = DIR_OUT + "c" + str(i) + ".out"
            p, solucion = IO.readFileOut(filename=caso)

            file.write(FMT_COLS.format(p, solucion[0], i)) 
            
 


if __name__ == "__main__":

    IO.createCSV(RESULTADOS, COLS)
    correr_potencia()
    medir()

    res = pd.read_csv(RESULTADOS)
    res.puntaje_testigo.describe().to_csv(SUMMARY)
    
    utils.graficar(
        x=res.q_nodos, 
        y=res.puntaje_testigo, 
        hue=["caso testigo"]*N, 
        xaxis="CANTIDAD DE PÁGINAS", 
        yaxis="PUNTAJE", 
        filename=GRAFICO)
