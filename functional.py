import json
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation
import matplotlib.patches as mpatches


def draw_social_graph():
    path = 'friends.json'  # data file
    G = nx.Graph()
    with open(path, 'r', encoding='UTF8') as f:
        data = json.loads(f.read())
    # data is read list of dictionaries

    # limits (can be variable for different data sizes); set for better visualisation
    first_level_limit = 150
    second_level_limits = 30
    # default node sizes
    node_size_2lvl = 10
    node_size_1lvl = 55
    node_size_target = 200
    # if tiny data
    if len(data[0]["friends"]) < 20:
        node_size_2lvl = 400
        node_size_1lvl = 800
        node_size_target = 1000
    for person in data:
        G.add_node(person["id"], **person)

    for person in data:
        for friend in person["friends"]:
            G.add_edge(person["id"], friend)

    target = data[0]["id"]  # id of target person

    GG = nx.Graph()  # graph for drawing

    sub_dict = {"id": G.nodes[target].setdefault("id", target),
                "first_name": G.nodes[target].setdefault("first_name", "?"),
                "last_name": G.nodes[target].setdefault("last_name", "?"),
                "friends": G.nodes[target].setdefault("friends", [])}
    GG.add_node(sub_dict["id"], **sub_dict)
    friend_list1 = []  # list of edges with 1st level friends
    target_friends = []  # list of ids of target's friends to draw
    counter1 = 0
    for friend1 in GG.nodes[target]["friends"]:
        counter1 += 1  # counter of 1st level friends
        if counter1 <= first_level_limit:  # limit of friends to draw
            sub_dict = {"id": G.nodes[friend1].setdefault("id", friend1),
                        "first_name": G.nodes[friend1].setdefault("first_name", "?"),
                        "last_name": G.nodes[friend1].setdefault("last_name", "?"),
                        "friends": G.nodes[friend1].setdefault("friends", [])}
            GG.add_node(sub_dict["id"], **sub_dict)
            GG.add_edge(target, friend1)
            friend_list1.append((friend1, target))  # add edge to list
            target_friends.append(friend1)
            counter2 = 0  # counter of 2nd level friends
            for friend2 in GG.nodes[friend1]["friends"]:
                if friend2 in GG.nodes[target]['friends']:
                    sub_dict = {"id": G.nodes[friend2].setdefault("id", friend2),
                                "first_name": G.nodes[friend2].setdefault("first_name", "?"),
                                "last_name": G.nodes[friend2].setdefault("last_name", "?"),
                                "friends": G.nodes[friend2].setdefault("friends", [])}
                    GG.add_node(sub_dict["id"], **sub_dict)
                    GG.add_edge(friend1, friend2)
                    GG.add_edge(target,friend2)
                else:
                    counter2 += 1
                if counter2 <= second_level_limits:  # limit for friends to draw
                    sub_dict = {"id": G.nodes[friend2].setdefault("id", friend2),
                                "first_name": G.nodes[friend2].setdefault("first_name", "?"),
                                "last_name": G.nodes[friend2].setdefault("last_name", "?"),
                                "friends": G.nodes[friend2].setdefault("friends", [])}
                    GG.add_node(sub_dict["id"], **sub_dict)
                    GG.add_edge(friend1, friend2)
                else:
                    break
        else:
            break
    fig = plt.figure()
    fig.canvas.set_window_title('social graph')
    fig.suptitle('Граф дружбы пользователя ' + GG.nodes[target]["last_name"] + ' ' + GG.nodes[target]["first_name"]
                 + '\n' + str(len(GG.nodes[target]['friends'])) + ' друзей', fontsize=13)  # title
    limits = plt.axis('off')  # don't show axis
    pos = nx.spring_layout(GG)  # generate position for each node
    labels = {}  # list of node labels
    for node in GG.nodes():
        if node in GG.nodes[target]["friends"] or node == target:
            labels[node] = GG.nodes[node]["last_name"] + ' ' + GG.nodes[node]["first_name"]  # long labels
        else:
            labels[node] = ''  # 2nd level friends have empty labels
    # drawing process
    nx.draw_networkx_edges(GG, pos=pos, labels=labels, edge_color='grey', alpha= 0.2)  # draw all the edges
    nx.draw_networkx_edges(GG, pos=pos, edge_color='grey', edgelist=friend_list1)  # draw edges with 1st level friends
    nx.draw_networkx_nodes(GG, pos=pos, node_size=node_size_2lvl)  # draw all nodes
    nx.draw_networkx_labels(GG, pos=pos, labels=labels, font_size=6)  # draw labels
    nx.draw_networkx_nodes(GG, pos, nodelist=target_friends, label=[labels[target]], node_color='r',
                           node_size=node_size_1lvl)  # draw nodes of 1st level friends red
    nx.draw_networkx_nodes(GG, pos, nodelist=[target], label=[labels[target]], node_color='#FFFC00',
                           node_size=node_size_target)  # neon yellow draw target
    #
    fig.set_size_inches(16, 9)  # set figure's size
    fig.tight_layout()  # маленькие отступы
    red_patch = mpatches.Patch(color='red', label='друзья первого уровня')
    blue_patch = mpatches.Patch(label='друзья второго уровня')  # default blue color
    plt.legend(handles=[red_patch, blue_patch])  # add graph legend
    # output files: friends.png and friends.html
    plt.savefig('friends.png', bbox_inches="tight")

    html = '<img src=\'friends.png\'>'
    with open('friends.html', 'w') as f:
        f.write(html)


def draw_social_path():
    path = 'way.json'  # data file
    G = nx.Graph()
    with open(path, 'r', encoding='UTF8') as f:
        data = json.loads(f.read())
    # data is read list of dictionaries

    # limits (can be variable for different data sizes); set for better visualisation
    level_limit = 40

    social_path = []
    for person in data:
        G.add_node(person["id"], **person)
        social_path.append(person["id"])

    for person in data:
        for friend in person["friends"]:
            G.add_edge(person["id"], friend)

    GG = nx.Graph()  # graph for drawing

    for point in social_path[0:len(social_path)]:
        sub_dict = {"id": G.nodes[point]["id"], "first_name": G.nodes[point]["first_name"],
                    "last_name": G.nodes[point]["last_name"], "friends": G.nodes[point]["friends"]}
        GG.add_node(sub_dict["id"], **sub_dict)

    level_limit = 40
    for i in range(0, len(social_path)):
        counter = 0  # number of friends for one person to draw
        if i != 0:
            GG.add_edge(social_path[i], social_path[i-1])  # add edges between social path points
        for friend in GG.nodes[social_path[i]]["friends"]:
            if G.degree[friend] > 1 and counter < level_limit:  # add friends who have more friends than 1
                counter += 1  # level_limit friends for one person to draw
                sub_dict = {"id": G.nodes[friend].setdefault("id", friend),
                            "first_name": G.nodes[friend].setdefault("first_name", "?"),
                            "last_name": G.nodes[friend].setdefault("last_name", "?"),
                            "friends": G.nodes[friend].setdefault("friends", [])}
                GG.add_node(sub_dict["id"], **sub_dict)
                GG.add_edge(social_path[i], friend)
        for friend in GG.nodes[social_path[i]]["friends"]:
            counter += 1
            if counter < level_limit:  # add rest of friends up to level_limit
                sub_dict = {"id": G.nodes[friend].setdefault("id", friend),
                            "first_name": G.nodes[friend].setdefault("first_name", "?"),
                            "last_name": G.nodes[friend].setdefault("last_name", "?"),
                            "friends": G.nodes[friend].setdefault("friends", [])}
                GG.add_node(sub_dict["id"], **sub_dict)
                GG.add_edge(social_path[i], friend)

    pos = nx.spring_layout(GG)  # generate position for each node
    labels = {}  # list of node labels
    for node in GG.nodes():
        if node not in social_path:
            labels[node] = GG.nodes[node]["id"]  # short labels id for friends not in social path

    fig = plt.figure()
    fig.set_size_inches(16, 9)  # set figure's size
    fig.canvas.set_window_title('way graph')
    fig.suptitle('Путь от пользователя ' + GG.nodes[social_path[0]]["last_name"] + ' ' +
                 GG.nodes[social_path[0]]["first_name"] + ' к пользователю ' + GG.nodes[social_path[-1]]["last_name"] +
                 ' ' + GG.nodes[social_path[-1]]["first_name"]+' (длина - '+str(len(social_path))+' человека)',
                 fontsize=13)  # graph title
    limits = plt.axis('off')  # don't show figure axis

    # drawing process
    nx.draw_networkx_edges(GG, pos=pos, labels=labels, edge_color='grey', style="solid")  # draw all the edges
    nx.draw_networkx_nodes(GG, pos=pos, node_size=100, node_color='#FFA500')  # draw all nodes as orange circles
    nx.draw_networkx_labels(GG, pos=pos, labels=labels, font_size=7)  # draw all labels

    path_labels = {}  # list of long labels for points in social path
    for point in social_path:
        path_labels[point] = GG.nodes[point]["last_name"] + ' ' + GG.nodes[point]["first_name"]  # add labels
    nx.draw_networkx_labels(GG, pos=pos, labels=path_labels, font_size=7, font_weight="bold")
    # draw labels for points in social path (bold)
    edge_list = []  # list of social path edges
    for i in range(0, len(social_path) - 1):
        edge_list.append((social_path[i], social_path[i + 1]))  # add edge
    nx.draw_networkx_edges(G, pos=pos, edgelist=edge_list, edge_color='r', style="solid", width=3)
    # draw red social path edges
    nx.draw_networkx_nodes(GG, pos=pos, nodelist=social_path, node_size=400, node_color='r', node_shape='*')
    # draw nodes-points in social path as red stars
    fig.tight_layout()  # маленькие отступы

    # output files: way.png and way.html
    plt.savefig('way.png', bbox_inches="tight")
    html = '<img src=\'way.png\'>'
    with open('way.html', 'w') as f:
        f.write(html)


def draw_social_groups():
    path = 'groups.json'  # data file
    G = nx.Graph()
    people_list = []  # list of users ids
    groups_list = []  # list of groups ids
    with open(path, 'r', encoding='UTF8') as f:
        data = json.loads(f.read())  # reading from the file
    # data is read list of dictionaries

    # count limit
    n = len(data)  # number of people in initial data
    groups_limit = n/10
    if n < 10:
        groups_limit = 10

    for person in data:
        G.add_node(person["id"], **person, bipartite=0)  # bipartite=0 person add node
        for group in person["groups"]:
            G.add_node(group["id"], **group, bipartite=1)  # bipartite=1 group or page add node
            G.add_edge(person["id"], group["id"])
    GG = nx.Graph()  # GG - graph for drawing
    for node in G.nodes():
        if G.nodes[node]['bipartite'] == 1 and G.degree[node] > groups_limit:  # take only "top" groups
            for person in G[node]:
                GG.add_node(person, **G.nodes[person])
                people_list.append(person)  # add user id to list
            GG.add_node(node, **G.nodes[node])
            groups_list.append(node)  # add group id to list
            GG.add_edges_from(G.edges(node))
    labels = {}  # list of node labels
    for node in GG.nodes():
        if GG.nodes[node]["bipartite"] == 0:
            labels[node] = G.nodes[node]["last_name"]+' '+G.nodes[node]["first_name"]  # long labels for users
        else:
            labels[node] = G.nodes[node]["name"]  # name of group labels
    table = []  # table with top groups statistics
    for group in GG.nodes():
        if GG.nodes[group]['bipartite'] == 1 and G.degree[group] > groups_limit:  # take only "top" groups
            table.append([GG.nodes[group]['name'], G.degree[group]])  # add group str to table
    # sorting groups by number of friends following
    for i in range(0, len(table)-1):
        for j in range(i, len(table)-1):
            if table[i][1] < table[j][1]:
                table[i], table[j] = table[j], table[i]

    l, r = nx.bipartite.sets(GG)  # sets of elements: l-for left column to draw, r-for right column to draw
    pos = {}  # positions for each nodes

    # update position for node from each group
    pos.update((node, (1, index)) for index, node in enumerate(l))
    pos.update((node, (2, index)) for index, node in enumerate(r))

    fig = plt.figure()
    ax = plt.subplot()
    fig.suptitle('Топ сообществ, пабликов и подписок среди друзей пользователя '+data[0]["last_name"]+' ' +
                 data[0]['first_name'], fontsize=13)  # title
    limits = plt.axis('off')  # don't show axis

    # drawing process
    nx.draw_networkx_nodes(GG, pos=pos, ax=ax, nodelist=people_list, node_color='#3CB371', node_size=100)
    # draw nodes of users (left column) as green circles
    nx.draw_networkx_nodes(GG, pos=pos, ax=ax, nodelist=groups_list, node_color='#DDA0DD', node_size=100)
    # draw nodes of groups (right column) as purple circles
    nx.draw_networkx_labels(GG, pos=pos, ax=ax, labels=labels, font_size=7)  # draw node's labels
    nx.draw_networkx_edges(GG, pos=pos, ax=ax, edge_color='grey', alpha=0.5)  # draw all edges

    fig.set_size_inches(16, 9)  # set figure's size
    plt.legend(labels=['пользователи', 'сообщества, паблики и подписки'])  # set legend
    ax.table(cellText=table, colLabels=['название', 'сколько друзей подписано'], loc='bottom')
    # draw table, colLabels as column titles

    fig.tight_layout()  # маленькие отступы
    # output files: groups.png and groups.html
    plt.savefig('groups.png', bbox_inches="tight")
    html = '<img src=\'groups.png\'>'
    with open('groups.html', 'w') as f:
        f.write(html)


# debugging #
# option = int(input())
# 1 social graph
# 2 social path
# 3 group
option = 1
if option == 1:
    draw_social_graph()
elif option == 2:
    draw_social_path()
elif option == 3:
    draw_social_groups()
