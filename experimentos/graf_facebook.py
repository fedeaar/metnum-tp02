import base.IO as IO

import ego_facebook as EGO

import pandas as pd
import numpy as np

import networkx as nx
import datashader as ds
import datashader.layout as layout
import datashader.bundling as bundling 

# ref: https://datashader.org/user_guide/Networks.html


def graficar_star(A, name, path, size=(1500, 1500)):
    
    # armamos lista de ejes y nodos
    nodes = pd.DataFrame([x for x in range(A.shape[0])])
    
    # agregamos central
    A = np.append(A, np.ones((1, A.shape[1])), axis=0)
    A = np.append(A, np.ones((A.shape[0], 1)), axis=1)
    A[A.shape[0] - 1, A.shape[0] - 1] = 0
    G = nx.from_numpy_array(A)
    edges = nx.to_pandas_edgelist(G)
    
    #definimos layout
    nodes_layout = layout.circular_layout(nodes, uniform=False) 
    nodes_layout.loc[len(nodes_layout)] = [
        0.0, 
        (nodes_layout.x.max() - nodes_layout.x.min()) / 2, 
        (nodes_layout.y.max() - nodes_layout.y.min()) / 2]  # add central
    edges_layout = bundling.hammer_bundle(nodes_layout, edges, decay=0.25, initial_bandwidth=0.5)

    # armamos canvas
    xr = nodes_layout.x.min() - 0.01, nodes_layout.x.max() + 0.01
    yr = nodes_layout.y.min() - 0.01, nodes_layout.y.max() + 0.01
    canvas = ds.Canvas(x_range=xr, y_range=yr, plot_height=size[0], plot_width=size[1])

    # plot nodos
    agg = canvas.points(nodes_layout,'x','y')
    shader = ds.transfer_functions.shade(agg, cmap=["#FF3333"])
    nplot = ds.transfer_functions.spread( # op: spread
            shader, 
            px=6,
            shape='circle', 
            how=None) 

    # plot ejes
    eplot = ds.transfer_functions.shade(canvas.line(edges_layout, 'x','y', agg=ds.count()))

    # unir
    img = ds.transfer_functions.Image(ds.transfer_functions.stack(eplot, nplot, how="over"))
    
    # save
    ds.utils.export_image(img=img, filename=name, fmt=".png", export_path=path, background='white')


def graficar_force(A, name, path, size=(1500, 1500)):

    # armamos lista de ejes y nodos
    G = nx.from_numpy_array(A)
    edges = nx.to_pandas_edgelist(G)
    nodes = pd.DataFrame([x for x in range(A.shape[0])])
    
    #definimos layout
    nodes_layout = layout.forceatlas2_layout(nodes, edges)       # op: random_layout, circular_layout, forceatlas2_layout 
    edges_layout = bundling.hammer_bundle(nodes_layout, edges)   # op: connect_edges
    
    # armamos canvas
    xr = nodes_layout.x.min() - 0.01, nodes_layout.x.max() + 0.01
    yr = nodes_layout.y.min() - 0.01, nodes_layout.y.max() + 0.01
    canvas = ds.Canvas(x_range=xr, y_range=yr, plot_height=size[0], plot_width=size[1])

    # plot nodos
    agg = canvas.points(nodes_layout,'x','y')
    shader = ds.transfer_functions.shade(agg, cmap=["#FF3333"])
    nplot = ds.transfer_functions.dynspread( # op: spread
            shader, 
            threshold=0.5, 
            max_px=3,
            shape='circle', 
            how=None) 

    # plot ejes
    eplot = ds.transfer_functions.shade(canvas.line(edges_layout, 'x','y', agg=ds.count()))

    # unir
    img = ds.transfer_functions.Image(ds.transfer_functions.stack(eplot, nplot, how="over"))
    
    # save
    ds.utils.export_image(img=img, filename=name, fmt=".png", export_path=path, background='white')




if __name__ == "__main__":
    
    A = IO.readMatriz(EGO.CLEAN_GRAFO)
    graficar_circular(A, name='grafo_circular_facebook', path=EGO.DIR)
    graficar_force(A, name='grafo_forceatlas2_facebook', path=EGO.DIR)
    for i in range(0, 13):
        file = EGO.GRAFO_SIM.format(u=f"{i}.0")
        print('graficando:', file)
        A = IO.readMatriz(file)
        graficar_circular(A, name=f"grafo_circular_{i}", path=EGO.DIR)
        graficar_force(A, name=f"grafo_forceatlas2_{i}", path=EGO.DIR)
