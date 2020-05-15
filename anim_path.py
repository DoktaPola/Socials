import json
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation

# data file
path = 'friends.json'
G = nx.Graph()
with open(path, 'r') as f:
    data = json.loads(f.read())

# example input
A_person = 242896860
B_person = 43745096

for person in data:
     G.add_node(person["id"], **person)

for person in data:
    for friend in person["friends"]:
        G.add_edge(person["id"], friend)

social_path = nx.shortest_path(G, source=A_person, target=B_person) # dijkstra
print("Path is:", social_path)
# graph for drawing
GG = nx.Graph()
for point in social_path[0:len(social_path)-1]:
    sub_dict = {"id": G.nodes[point]["id"], "first_name": G.nodes[point]["first_name"], "last_name":G.nodes[point]["last_name"], "friends": G.nodes[point]["friends"]}
    GG.add_node(sub_dict["id"], **sub_dict)
    sub_dict.clear()
sub_dict = {"id": G.nodes[social_path[-1]].setdefault("id", social_path[-1]), "first_name": G.nodes[social_path[-1]].setdefault("first_name", "?"),
            "last_name" : G.nodes[social_path[-1]].setdefault("last_name", "?"), "friends": G.nodes[social_path[-1]].setdefault("friends", [])}
GG.add_node(sub_dict["id"], **sub_dict)
sub_dict.clear()
for i in range(0,len(social_path)):
    counter = 0 # number of friends for one person to draw
    for friend in GG.nodes[social_path[i]]["friends"]:
        counter += 1
        if (counter < 50):
            sub_dict = {"id": G.nodes[friend].setdefault("id", friend),
                        "first_name": G.nodes[friend].setdefault("first_name", "?"),
                        "last_name": G.nodes[friend].setdefault("last_name", "?"),
                        "friends": G.nodes[friend].setdefault("friends", [])}
            GG.add_node(sub_dict["id"], **sub_dict)
            GG.add_edge(social_path[i], friend)
    if(i != len(social_path)-1):
        GG.add_edge(social_path[i], social_path[i+1])

pos = nx.spring_layout(GG)
labels = {}
for node in GG.nodes():
    labels[node] = GG.nodes[node]["last_name"][0]+'.'+GG.nodes[node]["first_name"][0]+'.' #short labels
for point in social_path:
    labels[point] = GG.nodes[point]["last_name"]+' '+GG.nodes[point]["first_name"] #long labels

fig, ax = plt.subplots()

def update(num): #animation function
    limits = plt.axis('off')
    hightlight = social_path[0:num]
    nx.draw_networkx_edges(GG, pos=pos, labels=labels, edge_color='grey')
    nx.draw_networkx_nodes(GG, pos=pos)
    nx.draw_networkx_labels(GG, pos=pos, labels=labels, font_size=9)
    edge_list = []
    for i in range(0, len(hightlight) - 1):
        edge_list.append((hightlight[i], hightlight[i + 1]))
    nx.draw_networkx_edges(G, pos=pos, edgelist=edge_list,
                           edge_color='r', style="solid")
    nx.draw_networkx_nodes(GG, pos=pos, nodelist=hightlight, node_color='r')

ani = matplotlib.animation.FuncAnimation(fig,update, frames = len(social_path)+1, interval=200, repeat=True)
plt.show()