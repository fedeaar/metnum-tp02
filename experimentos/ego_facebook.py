import base.IO as IO

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


"""
descripcion: 
    Aproximación por matriz de similaridad con producto interno y
    análisis de componentes principales (PCA) para la 
    red-ego de Facebook.
"""


# IO
EXPERIMENTO = "ego-facebook"
DIR_IN, DIR_OUT, DIR = IO.createInOut(EXPERIMENTO)

# VARS
GRAFO = "../catedra/ego-facebook.edges"
ATRIBUTOS = "../catedra/ego-facebook.feat"

# OUTPUT
SIMILARIDAD   = DIR + "facebook_similaridad_{u}.txt"

# UTILS

def similaridad_to_grafo(sim, col):
    links = np.where(sim != 0)
    links = tuple(zip(*links))
    text  = []
    for coord in links:
        text.append(str(col[coord[1]]) + " " + str(col[coord[0]]))
    return text

def correlacion_adyacencia(aproximado, original):

    A = IO.readGrafo(aproximado)
    O = IO.readGrafo(original)

    # Pueden tener diferente tamaño
    n = np.size(O, 0)
    m = np.size(A, 0)
    faltantes = n - m
    A = np.pad(A, ((0 , faltantes), (0 , faltantes)))

    # Elimino filas con tags invalidas
    A = A[~np.all(O == 0, axis=1)]
    O = O[~np.all(O == 0, axis=1)]
    A = A[:,~np.all(O == 0, axis=0)]
    O = O[:,~np.all(O == 0, axis=0)]

    A.flatten()
    O.flatten()
    total = O.size

    return np.count_nonzero(A == O) / total

def correlacion_autovalores(aproximado, original):

    A = IO.readGrafo(aproximado)
    O = IO.readGrafo(original)

    # Pueden tener diferente tamaño
    n = np.size(O, 0)
    m = np.size(A, 0)
    faltantes = n - m
    A = np.pad(A, ((0 , faltantes), (0 , faltantes)))

    # Elimino filas con tags invalidas
    A = A[~np.all(O == 0, axis=1)]
    O = O[~np.all(O == 0, axis=1)]
    A = A[:,~np.all(O == 0, axis=0)]
    O = O[:,~np.all(O == 0, axis=0)]

    w1, V1 = np.linalg.eig(A)
    w2, v2 = np.linalg.eig(O)

    idx = np.argsort(w1)[::-1]
    idx = np.argsort(w2)[::-1]

    r = np.corrcoef(w1, w2)[0][1].real
    
    return r


# EXP

def aproximar_similaridad():
    col, X = IO.readAtributos(ATRIBUTOS)
    S = X @ X.T
    # El minimo va a ser 0 ya que atributos tiene 1s y 0s
    umbrales = np.arange(0, np.max(S), 2)
    corr_ady = []
    corr_autov = []
    
    for u in umbrales:
        T = S
        T = (T > u).astype(int)
        T = T - np.diag(np.diag(T)) # Quito autoconexiones
        # Poscion i,j corresponde a la conexion entre col[i] y col[j]
        grafo = similaridad_to_grafo(T, col) 
        # Si hay al menos una conexion
        if grafo: 
            path = SIMILARIDAD.format(u = u)
            #np.savetxt(path, grafo, delimiter="\n", fmt="%s") 
            corr_ady.append((u, correlacion_adyacencia(path, GRAFO)))
            corr_autov.append((u, correlacion_autovalores(path, GRAFO)))
    print(corr_ady)
    print(corr_autov)

def pca():

    # Primero calculo autovectores de matriz de covarianza
    col, X = IO.readAtributos(ATRIBUTOS)
    Xcentered = X - X.mean(0)
    n = np.size(Xcentered, 0)
    M = (Xcentered.T@Xcentered) / (n-1)
    a, V = np.linalg.eig(M)
    idx = np.argsort(a)[::-1]
    a = a[idx]
    V = V[:,idx] 

    # Deberian estar ordenados de mayor a menor
    # A es de m x n
    # M es de n x n
    # -> autovalores son de largo n
    # A * autovalor(M) se puede hacer
    
    # Observo los diferentes valores de suma acumulada de varianza
    acc = np.cumsum(a / np.sum(a)).real
    precisiones = np.array([0.5, 0.75, 0.8, 0.85, 0.9, 0.95, 0.99])
    for i in precisiones:
        k = np.where(acc > i)
        print(f"Autovectores para representar el {i * 100}%: ", k[0][0])
    print("Total de autovectores:", acc.size)

    # Para empezar voy a tomar k tal que represento el 90%
    k = np.where(acc > 0.9)[0][0]
    A = (X @ V[:,:k]).real # Genera nueva matriz de n x k 
    
    # Calculo matriz de similaridad
    D = A @ A.T
    # Algunos tests despues borro
    #print(D)
    #positivos = (D > 0).sum()
    #print(positivos)
    #negativos = (D < 0).sum()
    #print(negativos)
    #print(D.size)
    #print(negativos + positivos)

if __name__ == "__main__":

    pass # TODO
