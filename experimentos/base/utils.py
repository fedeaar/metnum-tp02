import base.IO

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(rc={'figure.figsize':(14, 7)}, font="Times New Roman")


# GLOBALES
EPSILON = 1e-4


def random_conectividad(n, cantidad, dirigida=True, seed=None):

    sz = (n - 1) * n if dirigida else n * (n - 1) // 2
    W = np.zeros(sz, dtype=np.double)
    W[:cantidad] = 1
    
    rng = np.random.default_rng(seed if seed else None)
    rng.shuffle(W)
    
    if dirigida:
        for i in range(0, sz, n + 1):
            W = np.concatenate((W[:i], [0], W[i:]))
        W = np.append(W, 0)
    else:
        for i in range(n):
            W = np.concatenate((W[:i*n], [0]*(i+1), W[i*n:]))
    
    W = W.reshape((n, n))
    
    if not dirigida:
        W = W + W.T

    return W 


def random_matriz(n, m=None, r=(1, 100)):

    return np.random.randint(r[0], r[1], (n, m if m else n))


def norma(x, norma):

    return np.linalg.norm(x, norma)


def metodo_potencia(A, niter=10000, epsilon=1e-6):

    n = A.shape[0]
    z = np.zeros((n, 1))
    
    x = np.random.rand(n, 1)
    if np.allclose(x, z, epsilon):
        x = z.copy()
        x[0] = 1
    else:
    	x = x / norma(x, 2)

    for _ in range(niter):
        y = A @ x
        n = norma(y, 2)
        if abs(n) < epsilon or norma(x - y / n, 2) < epsilon:
        	break
        x = y / n
    a = (x.T @ A @ x) / (x.T @ x)

    return a[0, 0], x


def metodo_deflacion(A, k, niter=10000, epsilon=1e-6):

    n = A.shape[0]
    A = A.copy()
    eigs = []
    vecs = np.zeros((n, k))

    for i in range(k):
        a, v = metodo_potencia(A, niter, epsilon)
        eigs.append(a)
        vecs[:, i] = v.T
        A = A - a * (v @ v.T)
        
    return np.array(eigs), vecs


def eig(A):

    w, V = np.linalg.eig(A)
    idx = np.argsort(np.abs(w))[::-1]
    w = w[idx]
    V = V[:, idx]
    return w, V


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
