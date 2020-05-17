import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation
import random
import numpy as np
from functools import partial

# creating graph
dictionary = {1: {'name': 'Marina', 'age': 18, 'friendlist': [2, 3,4,5,6,7,8]},
              2: {'name': 'Lena', 'age': 17, 'friendlist': [1, 3,5,7]},
              3: {'name': 'Masha', 'age': 19, 'friendlist': [1, 2,5,7]},
              4: {'name': 'Ivan', 'age': 25, 'friendlist': [1,6]},
              5: {'name': 'Polina', 'age': 18, 'friendlist': [1, 2, 3, 7]},
              6: {'name': 'Daniel', 'age': 25, 'friendlist': [1,4,7,8]},
              7: {'name': 'Alex', 'age': 21, 'friendlist': [1,2, 3, 5, 6,8]},
              8: {'name': 'Olga', 'age': 29, 'friendlist': [1, 7, 6]},
              }
G = nx.Graph()
for value in dictionary.values():
    G.add_node(value['name'])
for value in dictionary.values():
    for i in value['friendlist']:
        G.add_edge(value['name'], dictionary[i]['name'])

# draw options
options = {
    'node_size': 1500,
    'with_labels': True,
    'pos': nx.spring_layout(G)
}


# functions
def update1(i, G, pos, t, ax):
    # fig.clf()
    cmap = matplotlib.cm.get_cmap('Blues')
    color_map = []
    for node in G:
        color_map.append(cmap(t[i]))
    nx.draw_networkx_nodes(G, pos, with_labels=True, node_color=color_map, ax=ax,node_size= 1500 )


# window1
fig1 = plt.figure()
nx.draw(G, **options)
# window2
fig2 = plt.figure()
colors = ['r', 'w', 'g', 'y', 'm', 'b', 'c']
nx.draw(G, node_color=[random.choice(colors) for j in range(8)], **options, edge_color="grey")
nx.draw_networkx_edges(G, edgelist=[('Marina', dictionary[i]['name']) for i in dictionary[1]['friendlist']],
                       width=5, edge_color="skyblue", style="solid", **options)
fig2.set_facecolor("#00000F")
t = np.linspace(0, 1, 10)
pos = nx.spring_layout(G)
# window3
fig3 = plt.figure()
ax = fig3.add_axes([0, 0, 1, 1])
plt.axis('off')
upd = partial(update1, G=G, pos=pos, t=t, ax=ax)
nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, ax=ax)
nx.draw_networkx_labels(G, pos)
ani = matplotlib.animation.FuncAnimation(fig3, upd, repeat=True, interval=100, frames=len(t), repeat_delay=10)

plt.show()
