import random
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import warnings

import networkx as nx
import pandas as pd

warnings.filterwarnings('ignore')


def generate_random_3Dgraph():
    table = pd.read_csv('C:\KURSACH\File_CSV.csv')

    FB = nx.from_pandas_edgelist(table, source='name', target='friend')  # создаю граф с ребрами без атрибутов
    row_count = len(table['name'])  # сколько строчек

    pos = {i: (random.uniform(0, 10), random.uniform(0, 5), random.uniform(0, 5)) for i in range(row_count)}

    for name in FB.nodes():  # заполняю nodes  данными
        visited = set()

        if name not in visited:
            visited.add(name)

            if name in list(table['name']):  # проверяю есть ли имя в таблице в столбце 'name'
                data = table.loc[table['name'] == name]  # ищу все строки с именем
                ind = data.index[0]  # считаю индекс первой строки с таким именем, для сбора всех данных

                FB.node[name]['id'] = data.id[ind]
                FB.node[name]['study'] = data.study[ind]
                FB.node[name]['live in'] = data['live in'][ind]
                FB.node[name]['links'] = data.links[ind]
                FB.node[name]['b-day'] = data['b-day'][ind]
                FB.node[name]['e-mail'] = data['e-mail'][ind]
                FB.node[name]['pos'] = pos[ind]
        else:
            continue

    return FB


def network_plot_3D(G, angle, save=False):
    USER = "Полина Ожиганова"
    # Get node positions
    pos = nx.get_node_attributes(G, 'pos')

    # add labels
    labels = []
    for k in G.nodes():
        l = k.replace(' ', '\n')
        labels.append(l)

    # Get the maximum number of edges adjacent to a single node
    edge_max = max([G.degree(node) for node in G.nodes()])
    # Define color range proportional to number of edges adjacent to a single node
    colors = [plt.cm.plasma(G.degree(node) / edge_max) for node in G.nodes()]

    # 3D network plot
    with plt.style.context(('ggplot')):

        fig = plt.figure(figsize=(10, 7))
        fig.suptitle('Facebook Network',
                     fontfamily='Comic Sans MS',
                     fontstyle='italic',
                     fontsize=24,
                     color='#ffffff')
        ax = Axes3D(fig)

        # Loop on the pos dictionary to extract the x,y,z coordinates of each node
        counter = 0
        for key, value in pos.items():
            xi = value[0]
            yi = value[1]
            zi = value[2]

            # Scatter plot
            if key == USER:
                ax.scatter(xi, yi, zi, c='#FF1493', s=20 + 20 * G.degree(key), edgecolors='k', alpha=0.7)
            else:
                ax.scatter(xi, yi, zi, c='#9370DB', s=20 + 20 * G.degree(key), edgecolors='k', alpha=0.7)
            # ax.scatter(xi, yi, zi, c=colors[key], s=20 + 20 * G.degree(key), edgecolors='k', alpha=0.7)
            ax.text(xi, yi, zi, labels[counter], color='#f7e6ff')
            counter += 1

        # Loop on the list of edges to get the x,y,z, coordinates of the connected nodes
        # Those two points are the extrema of the line to be plotted
        for i, j in enumerate(G.edges()):

            try:
                x = np.array((pos[j[0]][0], pos[j[1]][0]))
                y = np.array((pos[j[0]][1], pos[j[1]][1]))
                z = np.array((pos[j[0]][2], pos[j[1]][2]))
            except:
                continue

                # Plot the connecting lines
            ax.plot(x, y, z, c='#00FF00', alpha=0.5)

    # Set the initial view
    ax.view_init(30, angle)

    # Hide the axes
    ax.set_axis_off()
    if save is not False:
        plt.savefig(':\scratch\\data\"+str(angle).zfill(3)+".png')
        plt.close('all')
    else:
        # get black background
        plt.gca().patch.set_facecolor('black')
        ax.w_xaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
        ax.w_yaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
        ax.w_zaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
        plt.show()


G = generate_random_3Dgraph()
network_plot_3D(G, 0, save=False)
