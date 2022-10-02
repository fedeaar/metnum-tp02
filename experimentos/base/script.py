import array
from random import random
from re import T
import numpy as np
from numpy import eye as eye
from numpy import zeros as zeros
from numpy import ones as ones
from numpy import transpose as tp
from numpy import trace as tz
from numpy import concatenate as ct

from numpy.linalg import inv
from numpy.linalg import norm
from numpy.linalg import cholesky as chk
from scipy.linalg import lu
from scipy.linalg import det
# ----------------------------------------
# I = eye(n) : identidad
# Z = zeros((n,n)) : ceros
# U = ones((n,n)) : unos

# A @ B : multiplicacion de matrices
# tz(A) : traza
# tp(A) : traspuesta
# ct(range(1, j))

# inv(a) : la inversa
# P, L, U = lu(A) : factorizacion LU
# norm(l, 2) : norma vectorial, y tambien matricial dependiendo del input
# L = chk(A) : factorizacion de cholesky de una sdp

# np.around(A, decimals=2) : redondea los resultados
# v.astype(int) cambia el vector a int

SEP = "\n-----------------------\n"
MN_DEFAULT = -4
MX_DEFAULT = 4
N_DEFAULT = 5
# ----------------------------------------

# ----------------------------------------


def ceros(n=N_DEFAULT, m=0):
    """
    Devuelve una matriz de ceros.
    """
    if not m:
        return zeros((n, n))
    return zeros((n, m))


def unos(n=N_DEFAULT, m=0):
    """
    Devuelve una matriz de unos.
    """
    if not m:
        return ones((n, n))
    return ones((n, m))


def ei(n=N_DEFAULT, i=1):
    return eye(n)[int(i-1)]


def Ei(n=N_DEFAULT, i=1, inverso=False):
    E = diag(ei(n, i))
    if inverso:
        E = eye(n) - E
    return E


def perm(v):
    """
    Dado un vector como [1,5,4,2,3] devuelve la matriz permutación correspondiente.
    """
    P = [ei(len(v), x) for x in v]
    return np.array(P)


def ranVec(n=N_DEFAULT, mn=MN_DEFAULT, mx=MX_DEFAULT):
    """
    Devuelve un vector aleatorio.
    """
    A = ranMat(1, n, mn, mx)[0]
    return A


def isVec(v):
    return ((isinstance(v, list) and not isinstance(v[0], list)) or 
           (isinstance(v, np.ndarray) and not isinstance(v[0], np.ndarray)))

def ranMat(n=N_DEFAULT, m=0, mn=MN_DEFAULT, mx=MX_DEFAULT):
    """
    Devuelve una matriz aleatoria.
    """
    if not m:
        m = n
    A = np.random.randint(mx+1-mn, size=(n, m))
    A += mn
    return A


def expand(A, arriba=0, abajo=0, izq=0, der=0, value=0, col=True):
    B = A.copy()
    if(isVec(A)): B = tp(np.array([B])) if col else np.array([B])
    B = np.pad(B, [(arriba, abajo), (izq, der)], mode='constant', constant_values=value)
    if(not col and not(arriba or abajo) and isVec(A)) : B = B[0]
    return B


def diag(v):
    """
    Dado un vector como [1,5,4,2,3] devuelve una matriz diagonal con esos valores.
    """
    A = eye(len(v))
    A = [v[i] * A[i] for i in range(len(v))]
    return np.array(A)


def triang(sup, n=N_DEFAULT, m=N_DEFAULT, mn=MN_DEFAULT, mx=MX_DEFAULT):
    """ 
    Devuelve una matriz triangular aleatoria.
    Si 'sup = False' es inferior sino es superior.
    """
    A = ranMat(n, m, mn, mx)
    for i in range(0, n):
        for j in range(0, i):
            A[i][j] = 0

    return A if(not sup) else tp(A)


def invConLu(n=N_DEFAULT, mn=MN_DEFAULT, mx=MX_DEFAULT):
    """
    Devuelve una matriz inversible que admite factorizacion LU con P = I
    """
    A = [[0]]
    while not det(A):
        A = ranMat(n, n, mn, mx)

    P, L, U = lu(A)
    return (tp(P) @ A, L, U)


def sdp(n):
    """
    Devuelve una matriz aleatoria 'simétrica definida positiva' de tamaño n*n.
    """
    A = ranMat(n, n, -1, 1)
    return A @ tp(A)


def printM(A):
    print(np.around(A, decimals=2))
    print(SEP)


def serie(list):
    """
    Dado un vector [x0, x1, x2, x3, x4, x5] devuelve un vector [x0..x1, x2..x3, x4..x5] (inclusive [])
    """
    v = []
    for i in range(0, len(list), 2) :
        v = ct((v, range(list[i], list[i+1]+1)))
    return v
# ----------------------------------------


# ----------------------------------------
n = N_DEFAULT
# ----------------------------------------


A, L, U = invConLu(n)
r = np.random.randint(1, n-1)
P = perm(serie([1, r-1, n, n, r, n-1]))
Z = Ei(n, n, True)
M = expand(ranVec(), izq = n-1)
B = A @ P @ Z + M 
H = inv(L) @ B
printM(H)