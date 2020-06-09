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
        if counter1 <= 100:
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
                if counter2 <= 30:
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
    nx.draw_networkx_nodes(GG, pos, nodelist=[target], label=[labels[target]], node_color='#FFFC00', node_size=200)  #neon yellow
    #
    fig.set_size_inches(16, 9)  # set figure's size manually to your full screen (32x18)
    fig.tight_layout()  # маленькие отступы
    red_patch = mpatches.Patch(color='red', label='друзья первого уровня')
    blue_patch = mpatches.Patch(label='друзья второго уровня') #default blue color
    plt.legend(handles=[red_patch, blue_patch])
    plt.savefig('friends.png',bbox_inches = "tight")
    html = '<img src=\'friends.png\'>'
    with open('friends.html', 'w') as f:
        f.write(html)

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

    # print(social_path)
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

            if G.degree[friend]>1 and counter < 40:
                counter += 1
                sub_dict = {"id": G.nodes[friend].setdefault("id", friend),
                            "first_name": G.nodes[friend].setdefault("first_name", "?"),
                            "last_name": G.nodes[friend].setdefault("last_name", "?"),
                            "friends": G.nodes[friend].setdefault("friends", [])}
                GG.add_node(sub_dict["id"], **sub_dict)
                GG.add_edge(social_path[i], friend)
        for friend in GG.nodes[social_path[i]]["friends"]:
            counter += 1
            if (counter < 40):
                sub_dict = {"id": G.nodes[friend].setdefault("id", friend),
                            "first_name": G.nodes[friend].setdefault("first_name", "?"),
                            "last_name": G.nodes[friend].setdefault("last_name", "?"),
                            "friends": G.nodes[friend].setdefault("friends", [])}
                GG.add_node(sub_dict["id"], **sub_dict)
                GG.add_edge(social_path[i], friend)
    pos = nx.spring_layout(GG)
    labels = {}
    for node in GG.nodes():
        if node not in social_path:
            labels[node] = GG.nodes[node]["id"]  # short labels
    # for point in social_path:
    #     labels[point] = GG.nodes[point]["last_name"] + ' ' + GG.nodes[point]["first_name"]  # long labels
    # fig, ax = plt.subplots()
    fig = plt.figure()
    fig.set_size_inches(16, 9)  # set figure's size manually to your full screen (32x18)
    fig.canvas.set_window_title('way graph')
    fig.suptitle('Путь от пользователя ' + GG.nodes[social_path[0]]["last_name"] + ' ' + GG.nodes[social_path[0]]["first_name"] +
                 ' к пользователю ' + GG.nodes[social_path[-1]]["last_name"] + ' ' + GG.nodes[social_path[-1]]["first_name"]+' (длина - '+str(len(social_path))+' человека)', fontsize=13)
    limits = plt.axis('off')
    nx.draw_networkx_edges(GG, pos=pos, labels=labels, edge_color='grey', style="solid")  # , alpha=0.6
    nx.draw_networkx_nodes(GG, pos=pos, node_size=100, node_color='#FFA500')  # , linewidths = 0.5
    nx.draw_networkx_labels(GG, pos=pos, labels=labels, font_size=7)
    path_labels={}
    for point in social_path:
        path_labels[point]=GG.nodes[point]["last_name"] + ' ' + GG.nodes[point]["first_name"]
    nx.draw_networkx_labels(GG, pos=pos, labels=path_labels, font_size=7, font_weight="bold")
    edge_list = []
    for i in range(0, len(social_path) - 1):
            edge_list.append((social_path[i], social_path[i + 1]))
    nx.draw_networkx_edges(G, pos=pos, edgelist=edge_list,
                               edge_color='r', style="solid")
    nx.draw_networkx_nodes(GG, pos=pos, nodelist=social_path, node_size=400, node_color='r', node_shape='*')  #(4,0,0),edgecolors='grey'


    fig.tight_layout()  # маленькие отступы
    # plt.show()
    plt.savefig('way.png', bbox_inches="tight")

    html = '<img src=\'way.png\'>'

    with open('way.html', 'w') as f:
        f.write(html)

def draw_social_groups():
    # data file
    path = 'groups.json'
    G = nx.Graph()
    people_list=[]
    groups_list=[]
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
        if G.nodes[node]['bipartite']==1 and G.degree[node]>10:#2 is optional
            for person in G[node]:
                GG.add_node(person,**G.nodes[person])
                people_list.append(person)
            GG.add_node(node,**G.nodes[node])
            groups_list.append(node)
            GG.add_edges_from(G.edges(node))
    labels={}
    for node in GG.nodes():
        if GG.nodes[node]["bipartite"]==0:
            labels[node]=G.nodes[node]["last_name"]+' '+G.nodes[node]["first_name"]
        else:
            labels[node]=G.nodes[node]["name"]
    table=[]
    for group in GG.nodes():
        if GG.nodes[group]['bipartite'] == 1 and G.degree[group] > 10:
            table.append([GG.nodes[group]['name'],G.degree[group]])
    print(table)
    for i in range(0,len(table)-1):
        for j in range(i,len(table)-1):
            if table[i][1]<table[j][1]:
                table[i],table[j]=table[j],table[i]
    print(table)
    l, r = nx.bipartite.sets(GG)
    pos = {}

    # Update position for node from each group
    pos.update((node, (1, index)) for index, node in enumerate(l))
    pos.update((node, (2, index)) for index, node in enumerate(r))

    fig = plt.figure()
    ax = plt.subplot()

    fig.suptitle('Топ сообществ, пабликов и подписок среди друзей пользователя '+data[0]["last_name"]+' '+data[0]['first_name'], fontsize=13)
    limits = plt.axis('off')
    # pos=nx.bipartite_layout(GG, nodes=GG.nodes())
    nx.draw_networkx_nodes(GG, pos=pos, ax=ax,nodelist=people_list,node_color='#3CB371', node_size=100)
    nx.draw_networkx_nodes(GG, pos=pos, ax=ax,nodelist=groups_list,node_color='#DDA0DD', node_size=100)
    nx.draw_networkx_labels(GG, pos=pos,ax=ax, labels=labels, font_size=7)
    nx.draw_networkx_edges(GG, pos=pos, ax=ax,edge_color='grey', alpha=0.5)
    fig.set_size_inches(16,9)  # set figure's size manually to your full screen (32x18)
    plt.legend(labels=['пользователи','сообщества, паблики и подписки'])
    # bx=plt.subplot()
    ax.table(cellText=table, colLabels=['название','сколько друзей подписано'], loc='bottom')

    fig.tight_layout()  # маленькие отступы
    plt.savefig('groups.png', bbox_inches="tight")

    html = '<img src=\'groups.png\'>'

    with open('groups.html', 'w') as f:
        f.write(html)

# option = int(input())
# 1 social graph
# 2 social path
# 3 group
option = 3
if (option == 1):
    draw_social_graph()
elif (option==2):
    draw_social_path()
elif(option==3):
    draw_social_groups()

