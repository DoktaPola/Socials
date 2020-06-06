import json
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation
import matplotlib.patches as mpatches

def draw_social_graph():
    # data file
    path = 'friends.json'
    G = nx.Graph()
    with open(path, 'r') as f:
        data = json.loads(f.read())

    for person in data:
        G.add_node(person["id"], **person)

    for person in data:
        for friend in person["friends"]:
            G.add_edge(person["id"], friend)

    target = data[0]["id"]  # id of target person

    # graph for drawing
    GG = nx.Graph()

    sub_dict = {"id": G.nodes[target].setdefault("id", target),
                "first_name": G.nodes[target].setdefault("first_name", "?"),
                "last_name": G.nodes[target].setdefault("last_name", "?"),
                "friends": G.nodes[target].setdefault("friends", [])}
    GG.add_node(sub_dict["id"], **sub_dict)
    counter1 = 0
    friend_list1 = []
    for friend1 in GG.nodes[target]["friends"]:
        counter1 += 1
        if(counter1 <= 200):
            sub_dict = {"id": G.nodes[friend1].setdefault("id", friend1),
                        "first_name": G.nodes[friend1].setdefault("first_name", "?"),
                        "last_name": G.nodes[friend1].setdefault("last_name", "?"),
                        "friends": G.nodes[friend1].setdefault("friends", [])}
            GG.add_node(sub_dict["id"], **sub_dict)
            GG.add_edge(target, friend1)
            friend_list1.append((friend1,target))
            counter2 = 0
            for friend2 in GG.nodes[friend1]["friends"]:
                if friend2 in GG.nodes[target]['friends']:
                    sub_dict = {"id": G.nodes[friend2].setdefault("id", friend2),
                                "first_name": G.nodes[friend2].setdefault("first_name", "?"),
                                "last_name": G.nodes[friend2].setdefault("last_name", "?"),
                                "friends": G.nodes[friend2].setdefault("friends", [])}
                    GG.add_node(sub_dict["id"], **sub_dict)
                    GG.add_edge(friend1, friend2)
                else:
                    counter2 += 1
                if (counter2 <= 30):
                    sub_dict = {"id": G.nodes[friend2].setdefault("id", friend2),
                                "first_name": G.nodes[friend2].setdefault("first_name", "?"),
                                "last_name": G.nodes[friend2].setdefault("last_name", "?"),
                                "friends": G.nodes[friend2].setdefault("friends", [])}
                    GG.add_node(sub_dict["id"], **sub_dict)
                    GG.add_edge(friend1, friend2)
    fig = plt.figure()
    fig.canvas.set_window_title('social graph')
    fig.suptitle('Граф дружбы пользователя ' + GG.nodes[target]["last_name"] + ' ' + GG.nodes[target]["first_name"] +'\n'+str(len(GG.nodes[target]['friends']))+' друзей', fontsize=13)
    limits = plt.axis('off')
    pos = nx.spring_layout(GG)
    labels = {}
    for node in GG.nodes():
        if node in GG.nodes[target]["friends"] or node == target:
            labels[node] = GG.nodes[node]["last_name"] + ' ' + GG.nodes[node]["first_name"]  # long labels
        else:
            labels[node] = ''
    nx.draw_networkx_edges(GG, pos=pos, labels=labels, edge_color='grey', alpha= 0.2)
    nx.draw_networkx_edges(GG, pos=pos, edge_color='grey', edgelist=friend_list1)
    nx.draw_networkx_nodes(GG, pos=pos, node_size=10)
    nx.draw_networkx_labels(GG, pos=pos, labels=labels, font_size=6)
    #
    nx.draw_networkx_nodes(GG, pos, nodelist=GG.nodes[target]["friends"], label=[labels[target]], node_color='r', node_size=55)
    #
    def highlight(num):  # animation function
        if num%2==0:
            nx.draw_networkx_nodes(GG, pos, nodelist=[target], label=[labels[target]], node_color='#FFFC00', node_size=200)  #neon yellow
        else:
            nx.draw_networkx_nodes(GG, pos, nodelist=[target], label=[labels[target]], node_color='#F9FFDD', node_size=200)  #light yellow

    ani = matplotlib.animation.FuncAnimation(fig, highlight, frames=2, interval=100,
                                             repeat=True)  # repeat=True
    mng = plt.get_current_fig_manager()
    mng.window.state("zoomed")
    fig.tight_layout()  # маленькие отступы
    red_patch = mpatches.Patch(color='red', label='друзья первого уровня')
    blue_patch = mpatches.Patch(label='друзья второго уровня') #default blue color
    plt.legend(handles=[red_patch, blue_patch])
    plt.show()

def draw_social_path():
    path = 'way.json'
    G = nx.Graph()
    with open(path, 'r') as f:
        data = json.loads(f.read())

    social_path = []
    for person in data:
        G.add_node(person["id"], **person)
        social_path.append(person["id"])

    for person in data:
        for friend in person["friends"]:
            G.add_edge(person["id"], friend)

    print(social_path)
    GG = nx.Graph()
    for point in social_path[0:len(social_path)]:
        sub_dict = {"id": G.nodes[point]["id"], "first_name": G.nodes[point]["first_name"],
                    "last_name": G.nodes[point]["last_name"], "friends": G.nodes[point]["friends"]}
        GG.add_node(sub_dict["id"], **sub_dict)
    for i in range(0, len(social_path)):
        counter = 0  # number of friends for one person to draw
        if i!=0:
            GG.add_edge(social_path[i],social_path[i-1])
        for friend in GG.nodes[social_path[i]]["friends"]:
            counter += 1
            if (counter < 20):
                sub_dict = {"id": G.nodes[friend].setdefault("id", friend),
                            "first_name": G.nodes[friend].setdefault("first_name", "?"),
                            "last_name": G.nodes[friend].setdefault("last_name", "?"),
                            "friends": G.nodes[friend].setdefault("friends", [])}
                GG.add_node(sub_dict["id"], **sub_dict)
                GG.add_edge(social_path[i], friend)
    pos = nx.spring_layout(GG)
    labels = {}
    for node in GG.nodes():
        labels[node] = GG.nodes[node]["id"]  # short labels
    for point in social_path:
        labels[point] = GG.nodes[point]["last_name"] + ' ' + GG.nodes[point]["first_name"]  # long labels
    # fig, ax = plt.subplots()
    fig = plt.figure()
    fig.canvas.set_window_title('way graph')
    fig.suptitle('Путь от пользователя ' + GG.nodes[social_path[0]]["last_name"] + ' ' + GG.nodes[social_path[0]]["first_name"] +
                 ' к пользователю ' + GG.nodes[social_path[-1]]["last_name"] + ' ' + GG.nodes[social_path[-1]]["first_name"]+'\n(длина - '+str(len(social_path))+' человека)', fontsize=13)
    limits = plt.axis('off')

    def update_path(num):  # animation function
        hightlight = social_path[0:num]
        nx.draw_networkx_edges(GG, pos=pos, labels=labels, edge_color='grey',style="solid")#, alpha=0.6
        nx.draw_networkx_nodes(GG, pos=pos, node_size=400, node_shape='*', node_color='#FFA500',edgecolors='grey') #, linewidths = 0.5
        nx.draw_networkx_labels(GG, pos=pos, labels=labels, font_size=7)
        edge_list = []
        for i in range(0, len(hightlight) - 1):
            edge_list.append((hightlight[i], hightlight[i + 1]))
        nx.draw_networkx_edges(G, pos=pos, edgelist=edge_list,
                               edge_color='r', style="solid")
        nx.draw_networkx_nodes(GG, pos=pos, nodelist=hightlight, node_size=400, node_color='r', node_shape='*')  #(4,0,0),edgecolors='grey'

    ani = matplotlib.animation.FuncAnimation(fig, update_path, frames=len(social_path) + 1, interval=300,
                                             repeat=True)  # repeat=True

    mng = plt.get_current_fig_manager()
    mng.window.state("zoomed")
    fig.tight_layout()  # маленькие отступы
    plt.show()

def draw_social_groups():
    # data file
    path = 'groups.json'
    G = nx.Graph()
    with open(path, 'r', encoding='UTF8') as f:
        data = json.loads(f.read())
    for person in data:
        G.add_node(person["id"], **person, bipartite=0) #bipartite=0 person
        for group in person["groups"]:
            G.add_node(group["id"],**group, bipartite=1) #bipartite=1 group or page
            G.add_edge(person["id"],group["id"])
    GG = nx.Graph()
    for node in G.nodes():
        # print(G.degree[node])
        # print(G.nodes[node]['bipartite'])
        if G.nodes[node]['bipartite']==1 and G.degree[node]>8:#2 is optional
            for person in G[node]:
                GG.add_node(person,**G.nodes[person])
            GG.add_node(node,**G.nodes[node])
            GG.add_edges_from(G.edges(node))
    labels={}
    for node in GG.nodes():
        if GG.nodes[node]["bipartite"]==0:
            labels[node]=G.nodes[node]["last_name"]+' '+G.nodes[node]["first_name"]
        else:
            labels[node]=G.nodes[node]["name"]
    rating=''
    for group in GG.nodes():
        if GG.nodes[group]['bipartite'] == 1 and G.degree[node] > 8:
            print()
              # сделать словарь? + сортировку + в строку
    l, r = nx.bipartite.sets(GG)
    pos = {}

    # Update position for node from each group
    pos.update((node, (1, index)) for index, node in enumerate(l))
    pos.update((node, (2, index)) for index, node in enumerate(r))

    fig = plt.figure()
    ax=plt.subplot()
    limits = plt.axis('off')
    # pos=nx.bipartite_layout(GG, nodes=GG.nodes())
    nx.draw_networkx_nodes(GG, pos=pos, node_size=100)
    nx.draw_networkx_labels(GG, pos=pos, labels=labels,font_size=7)
    nx.draw_networkx_edges(GG, pos=pos, edge_color='grey', alpha=0.5)
    plt.legend(labels=['1','2'])
    # plt.text(1,0.5,'cnfnbcnbrf\nthn\ntrfgbhyn\ntrtbynumytrb\nrbtfyugtfrtgy\n')
    ax.text(.8,.8,'rotaыавОted   score\nwith newlines(8)\nynrjmnujmynuh(9)\nrynjumtk\nhrynjmutk\nthynrjmuk\nbhrtnyjtmuk\nebthrynjmu\nbgthrynjtum\ngbthynrjmu\nrgbtehnryjmu\nrgbthrynujm\n',
            fontsize=7)
    # nx.draw(GG, pos=pos, labels=labels)
    mng = plt.get_current_fig_manager()
    mng.window.state("zoomed")
    fig.tight_layout()  # маленькие отступы
    plt.show()

# option = int(input())
# 1 social graph
# 2 social path
# 3 group
option = 1
if (option == 1):
    draw_social_graph()
elif (option==2):
    draw_social_path()
elif(option==3):
    draw_social_groups()

