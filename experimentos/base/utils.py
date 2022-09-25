import base.IO

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(rc={'figure.figsize':(14, 7)}, font="Times New Roman")



# GLOBALES
EPSILON = 1e-4


def random_W(n, cantidad, seed=0):

    sz = (n-1)*n
    W  = np.zeros(sz, dtype=np.double)
    W[:cantidad] = 1

    rng = np.random.default_rng(seed if seed else None)
    rng.shuffle(W)
    
    for i in range(0, sz, n + 1):
        W = np.concatenate((W[:i], [0], W[i:]))
    W = np.append(W, 0)
    W = W.reshape((n, n))

    return W 


def norma_inf(x):

    return np.linalg.norm(x, np.inf)


def norma_uno(x):

    return np.linalg.norm(x, 1)


def solve(A, b):

    x = np.linalg.solve(A, b)
    
    return x


def graficar(x, y, hue, xaxis, yaxis, filename):
    
    plt.figure()
    df   = pd.DataFrame({"x":x, "y":y, "hue":hue})
    plot = sns.lineplot(data=df, x="x", y="y", hue="hue")
    
    plot.set_xlabel(xaxis, fontsize=18, labelpad=12)
    plot.set_ylabel(yaxis, fontsize= 18, labelpad=20) 
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.legend(title=None)

    fig = plot.get_figure()
    fig.savefig(filename)
