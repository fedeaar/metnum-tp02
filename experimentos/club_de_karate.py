import networkx as nx
import numpy as np
import base.IO as IO
import base.utils as utils
import matplotlib.pyplot as plt



def corr(x, y, epsilon=1e-16):
    xc = x - x.mean()
    yc = y - y.mean()
    a = xc.T @ yc
    b = np.sqrt((xc**2).T @ (yc**2))
    return a / b if abs(b) >= epsilon else 0


karate = IO.readMatriz("../catedra/karateclub_matriz.txt")
labels = IO.readMatriz("../catedra/karateclub_labels.txt")
#print(karate)
# G = nx.from_numpy_array(karate)
# f = plt.figure(figsize=(20, 10))
# nx.draw(G, with_labels=True, ax=f.add_subplot())
# f.savefig("graph.png")

# centralidad de autovector
# a, v = utils.metodo_potencia(karate, 10000, 1e-10)
# print(a, v)
# print(np.allclose(karate @ v, a * v, 1e-06, 1e-06))

# matriz 
D = np.diag([np.sum(x) for x in karate])
L = D - karate
print(np.allclose(L, L.T))
w, V = np.linalg.eig(L)#utils.metodo_deflacion(L, L.shape[0], 10000, 1e-10)
# print(w, '!')
# for i in range(len(w)):
#     #print(L @ V[:, i])
#     #print(w[i] * V[:, i])
#     print(i, np.allclose(L @ V[:, i], w[i] * V[:, i], 1e-06, 1e-06))

print(w, '\n\n')
mi, mw, mc = 0, w[0], abs(corr(V[:, 0], labels))
for i in range(V.shape[0]):
    tmp = corr(V[:, i], labels)
    if abs(tmp) > mc:
        mi, mw, mc = i, w[i], tmp
print(mi, mw, mc)

