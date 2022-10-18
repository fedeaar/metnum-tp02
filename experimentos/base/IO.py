import os
import shutil
import subprocess as sub
import numpy as np


# GLOBALES
EXE_PATH = '../build/tp2'      # si se compilo de otra manera o con otro nombre, cambiar por la direccion correcta
WSL = True                     # dejar true solo si se utilizó wsl para compilar el programa, false sino


def readGrafo(filename):
    
    with open(filename) as file:
        data = file.read().splitlines()
        links = [int(y) for x in data for y in x.split(' ')]
        n = np.max(links)
        matriz = np.zeros((n, n))
        for i in range(0, len(links), 2):
            matriz[links[i+1] - 1][links[i] - 1] = 1

    return matriz


def writeGrafo(filename, matrix):
    
    links = np.where(matrix != 0)
    links = tuple(zip(*links))
    text  = []
    for coord in links:
        text.append(str(coord[1] + 1) + " " + str(coord[0] + 1))

    np.savetxt(filename, text, delimiter="\n", fmt="%s")

    return links


def readMatriz(filename, cols=None):

    return np.loadtxt(filename, usecols=cols) 


def writeMatriz(A, filename):

    np.savetxt(filename, A)


def readTime(filename):

    with open(filename) as file:
        data = file.read().splitlines()
        scale = data[0]
        time = int(data[1])
        
    return scale, time


def readAutovalores(filename):

    return readMatriz(filename)


def readAutovectores(filename):
    
    return readMatriz(filename)


def writeAutovalores(niter, tol, eig, filename):

    data = [len(eig), niter, tol, *eig]
    np.savetxt(filename, data)


def writeAutovectores(A, filename):

    writeMatriz(A, filename)


def createInOut(filename, delete=False):
    
    path = "./resultados/" + filename + "/"
    pathIn =  path + "in/"
    pathOut = path + "out/"
    if delete and os.path.exists(path): 
        shutil.rmtree(path)
    if not os.path.exists(pathIn):
        os.makedirs(pathIn)
    if not os.path.exists(pathOut):
        os.makedirs(pathOut)
        
    return pathIn, pathOut, path


def createCSV(filename, columnas): 

    with open(filename, "w", encoding="utf-8") as file:
        file.write(columnas + "\n")


def run(filename, iter, epsilon, 
        f="matriz", o="./", precision=15, save_as=None, time=False, verbose=False,
        exe_path=EXE_PATH): # TODO: test

    call_params = [
        "wsl" if WSL else "",   
        exe_path, 
        filename, str(iter), str(epsilon),
        "-f", f"{f}",
        "-o", f"{o}",
        f"{'-as' if save_as else ''}", f"{save_as}" if save_as else "", 
        f"-presicion", f"{precision}", 
        "-time" if time else "",
        "-v" if verbose else ""
    ]
    sub.check_call(call_params)
