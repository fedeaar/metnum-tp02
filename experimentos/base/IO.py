import os
import subprocess as sub
import numpy as np


# GLOBALES
EXE_PATH = '../build/tp2'      # si se compilo de otra manera o con otro nombre, cambiar por la direccion correcta
WSL = True                     # dejar true solo si se utilizó wsl para compilar el programa, false sino


def readFileIn(filename):   # TODO
    pass


def readFileOut(filename):  # TODO
    pass


def readMatriz(filename):   # TODO
    pass


def readTime(filename):     # TODO
    pass


def createFileIn(filename, matrix): # TODO
    pass


def createInOut(filename):
    
    path = "./resultados/" + filename + '/'
    pathIn =  path + "in/"
    pathOut = path + "out/"
    if not os.path.exists(pathIn):
        os.makedirs(pathIn)
    if not os.path.exists(pathOut):
        os.makedirs(pathOut)
        
    return pathIn, pathOut, path


def createCSV(filename, columnas): 

    with open(filename, "w", encoding="utf-8") as file:
        file.write(columnas + '\n')


def run(filename, iter, thres, 
        out_dir="./", precision=15, save_as=None, time_it=False, save_m=False, 
        exe_path=EXE_PATH): # TODO

    # call_params = [
    #     "wsl" if WSL else "",   
    #     exe_path, 
    #     filename, str(p_value), 
    #     f"-out={out_dir}",
    #     f'{f"-save_as={save_as}" if save_as else ""}', 
    #     f"-presicion={precision}", 
    #     f'{"-time_it" if time_it else ""}',
    #     f'{"-save_m" if save_m else ""}'
    # ]
    # sub.check_call(call_params)
