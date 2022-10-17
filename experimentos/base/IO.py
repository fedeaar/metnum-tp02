import os
import subprocess as sub
import numpy as np


# GLOBALES
EXE_PATH = '../build/tp2'      # si se compilo de otra manera o con otro nombre, cambiar por la direccion correcta
WSL = True                     # dejar true solo si se utilizó wsl para compilar el programa, false sino


def readGrafo(filename):  # TODO: test
    
    with open(filename) as file:
        data = file.read().splitlines()
        n = int(data[0])
        q = int(data[1])
        links  = [x.split(' ') for x in data[2:]]
        matriz = np.zeros((n, n))
        for link in links:
            if (len(link) == 2):
                matriz[int(link[1]) - 1][int(link[0]) - 1] = 1

    return n, q, matriz # nodos, links, matriz de conectividad


def readAutovalores(filename):

    return readMatriz(filename)


def readAutovectores(filename):
    
    return readMatriz(filename)                 # cada columna es un autovector


def readTime(filename):

    with open(filename) as file:
        data = file.read().splitlines()
        scale = data[0]
        time = int(data[1])
        
    return scale, time


def readMatriz(filename, cols=None):

    return np.loadtxt(filename, usecols=cols) 


def writeMatriz(A, filename):

    np.savetxt(filename, A)


def writeGrafo(filename, matrix): # TODO: test
    
    n = matrix.shape[0]
    q = np.count_nonzero(matrix != 0)
    links = np.where(matrix != 0)
    links = tuple(zip(*links))
    text  = [n, q]
    for coord in links:
        text.append(str(coord[1] + 1) + " " + str(coord[0] + 1))

    np.savetxt(filename, text, delimiter="\n", fmt="%s")

    return links


def writeAutovalores(niter, tol, eig, filename):

    data = [len(eig), niter, tol, *eig]
    np.savetxt(filename, data)


def writeAutovectores(A, filename):

    writeMatriz(A, filename)


def createInOut(filename):
    
    path = "./resultados/" + filename + "/"
    pathIn =  path + "in/"
    pathOut = path + "out/"
    if not os.path.exists(pathIn):
        os.makedirs(pathIn)
    if not os.path.exists(pathOut):
        os.makedirs(pathOut)
        
    return pathIn, pathOut, path


def createCSV(filename, columnas): 

    with open(filename, "w", encoding="utf-8") as file:
        file.write(columnas + "\n")


def run(filename, iter, epsilon, 
        f="matriz", o="./", precision=15, save_as=None, time=False,
        exe_path=EXE_PATH): # TODO: test

    call_params = [
        "wsl" if WSL else "",   
        exe_path, 
        filename, str(iter), str(epsilon),
        "-f", f"{f}",
        "-o", f"{o}",
        f"{'-as' if save_as else ''}", f"{save_as}" if save_as else "", 
        f"-presicion", f"{precision}", 
        "-time" if time else ""
    ]
    sub.check_call(call_params)
