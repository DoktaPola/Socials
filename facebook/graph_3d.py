import json
import os
import random
import re
import warnings
from collections import deque

import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

warnings.filterwarnings('ignore')
csfont = {'fontname': 'Comic Sans MS'}

################## GLOBAL ##############################
labels = []
table = pd.read_csv('C:\KURSACH\File_CSV.csv')
# table = pd.read_csv('C:\KURSACH\Alena_Popova_CSV.csv')
# table = pd.read_csv('C:\KURSACH\KOLYA_CSV.csv')
row_count = len(table['name'])  # сколько строчек

USER = table['name'][0]


def create_graph_3D():
    FB = nx.from_pandas_edgelist(table, source='name', target='friend')  # создаю граф с ребрами без атрибутов
    pos = {i: (random.uniform(15, 20), random.uniform(15, 25), random.uniform(0, 20)) for i in range(row_count)}

    for name in FB.nodes():  # fill data in nodes
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
                # position = pos.get(name)
                # FB.node[name]['pos'] = position
            # elif name in list(table['friend']):  # друзья друзей
            #     if FB.degree(name) > 1:  # add only people whose degree is bigger then 1
            #         data_fr = table.loc[table['friend'] == name]  # ищу все строки с именем
            #         ind_fr = data_fr.index[0]  # считаю индекс первой строки с таким именем, для сбора всех данных
            #         FB.node[name]['pos'] = pos[ind_fr]
        else:
            continue
    return FB


def draw_graph_3D(G, angle):
    # Get node positions
    pos = nx.get_node_attributes(G, 'pos')

    # Add labels
    for k in G.nodes():
        l = k.replace(' ', '\n')
        labels.append(l)

    # Get the maximum number of edges adjacent to a single node
    edge_max = max([G.degree(node) for node in G.nodes()])

    # 3D network plot
    with plt.style.context(('ggplot')):

        fig = plt.figure(figsize=(100, 80))
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
            if key == USER:  # draw the main person
                ax.scatter(xi, yi, zi, c='#FF1493', s=20 + 20 * G.degree(key), edgecolors='k', alpha=0.7)
                ax.text(xi, yi, zi, labels[counter], color='#FF0000')
                counter += 1
            else:
                ax.scatter(xi, yi, zi, c='#9370DB', s=20 + 20 * G.degree(key), edgecolors='k', alpha=0.7)
                if G.degree(key) > 5:
                    ax.text(xi, yi, zi, labels[counter], color='#f7e6ff')  # ТОЛЬКО ДЛЯ ТЕХ, У КОГО МНОГО ДРУЗЕЙ
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

    return ax


###################################################################
#                      Network Analysis
###################################################################

def show_graph(ax):
    # Hide the axes
    ax.set_axis_off()

    # get black background
    plt.gca().patch.set_facecolor('black')
    ax.w_xaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
    ax.w_yaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
    ax.w_zaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
    plt.show()


def get_key(d, value):  # return key
    for k, v in d.items():
        if v == value:
            finale = k
            d.pop(k)
            return finale


def work_study(G, attr, info, my_ax):
    pos = nx.get_node_attributes(G, 'pos')

    study = []
    attr2 = attr.copy()  # работаю с копией словаря, чтобы удалять элементы
    for a in attr.values():  # try to find key
        info_lower = info.lower()
        a_lower = str(a).lower()
        if re.search(r"[а-яА-Яa-zA-Z]*\s?%s\s?[а-яА-Яa-zA-Z]*" % info_lower, a_lower):
            study.append(get_key(attr2, a))

    for key, value in pos.items():
        if not study:  # if study doesn't exist
            #########################
            # LEGEND
            fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='y', marker='x')
            my_ax.legend([fake2Dline], ['- no such place'], loc='upper right',
                         title='WARNING:'.format(info), numpoints=1, facecolor='#9370DB')
            ##########################
            break
        if key in study:
            ########################
            # LEGEND
            fake2Dline = mpl.lines.Line2D([], [], linestyle="none", c='#00BFFF', marker='o')
            legend_elements = []
            for f in range(0, len(study)):
                legend_elements.append(fake2Dline)

            labels = [f'{s}' for s in study]
            my_ax.legend(handles=legend_elements, labels=labels, loc='upper right',
                         title='Study: {}'.format(info), numpoints=1, facecolor='#9370DB')
            ##########################
            xi = value[0]
            yi = value[1]
            zi = value[2]

            # Scatter plot
            my_ax.scatter(xi, yi, zi, c='#00BFFF', s=20 + 20 * G.degree(key), edgecolors='k',
                          alpha=0.75)  # change node color
            if key != USER:
                my_ax.text(xi, yi, zi, key.replace(' ', '\n'), color='#00BFFF')  # change label color

    show_graph(my_ax)  # показывает граф


def work_live_in(G, attr, info, my_ax):
    pos = nx.get_node_attributes(G, 'pos')

    live_in = []
    attr2 = attr.copy()  # работаю с копией словаря, чтобы удалять элементы
    for a in attr.values():  # try to find key
        info_lower = info.lower()
        a_lower = str(a).lower()
        if re.search(r"[а-яА-Яa-zA-Z]*\s?%s\s?[а-яА-Яa-zA-Z]*" % info_lower, a_lower):
            live_in.append(get_key(attr2, a))

    for key, value in pos.items():
        if not live_in:  # if live_in doesn't exist
            ######################
            # LEGEND
            fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='y', marker='x')
            my_ax.legend([fake2Dline], ['- no information'], loc='upper right',
                         title='WARNING:'.format(info), numpoints=1, facecolor='#9370DB')
            ######################
            break
        if key in live_in:
            ######################
            # LEGEND
            fake2Dline = mpl.lines.Line2D([], [], linestyle="none", c='#FFFF00', marker='o')
            legend_elements = []
            for f in range(0, len(live_in)):
                legend_elements.append(fake2Dline)

            labels = [f'{s}' for s in live_in]
            my_ax.legend(handles=legend_elements, labels=labels, loc='upper left',
                         title='Live in: {}'.format(info), numpoints=1, facecolor='#9370DB')
            ########################
            xi = value[0]
            yi = value[1]
            zi = value[2]

            # Scatter plot
            my_ax.scatter(xi, yi, zi, c='#FFFF00', s=20 + 20 * G.degree(key), edgecolors='k',
                          alpha=0.75)  # change node color
            if key != USER:
                my_ax.text(xi, yi, zi, key.replace(' ', '\n'), color='#FFFF00')  # change label color

    show_graph(my_ax)  # показывает граф


def work_b_day(G, attr, info, my_ax):
    pos = nx.get_node_attributes(G, 'pos')

    b_day = []
    attr2 = attr.copy()  # работаю с копией словаря, чтобы удалять элементы
    for a in attr.values():  # try to find key
        if info.isalpha():
            _inf = info[:-1]
            info_lower = _inf.lower()
        else:
            info_lower = info.lower()
        a_lower = str(a).lower()

        if re.search(r"[а-яА-Яa-zA-Z0-9]*\s?%s\s?[а-яА-Яa-zA-Z0-9]*" % info_lower, a_lower):
            b_day.append(get_key(attr2, a))

    for key, value in pos.items():
        if not b_day:  # if b_day doesn't exist
            ##########################
            # LEGEND
            fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='y', marker='x')
            my_ax.legend([fake2Dline], ['- no information'], loc='upper right',
                         title='WARNING:'.format(info), numpoints=1, facecolor='#9370DB')
            ##########################
            break
        if key in b_day:
            ########################
            # LEGEND
            fake2Dline = mpl.lines.Line2D([], [], linestyle="none", c='#FF8C00', marker='o')
            legend_elements = []
            for f in range(0, len(b_day)):
                legend_elements.append(fake2Dline)

            labels = [f'{s}' for s in b_day]
            my_ax.legend(handles=legend_elements, labels=labels, loc='lower left',
                         title='Live in: {}'.format(info), numpoints=1, facecolor='#9370DB')
            ##########################
            xi = value[0]
            yi = value[1]
            zi = value[2]

            # Scatter plot
            my_ax.scatter(xi, yi, zi, c='#FF8C00', s=20 + 20 * G.degree(key), edgecolors='k',
                          alpha=0.75)  # change node color
            if key != USER:
                my_ax.text(xi, yi, zi, key.replace(' ', '\n'), color='#FF8C00')  # change label color

    show_graph(my_ax)  # показывает граф


def find_by_info(G, column, info, my_ax):  # нахожу в графе инфу по заданному
    attr = nx.get_node_attributes(G, column)

    if column == 'study':
        work_study(G, attr, info, my_ax)
    if column == 'live in':
        work_live_in(G, attr, info, my_ax)
        pass
    if column == 'b-day':
        work_b_day(G, attr, info, my_ax)
        pass


def find_connection(G, main_person, needed_person):  # bfs till 2nd level of friends
    path = []

    count_stars = 0
    friends_queue = deque()
    friends_queue += G[main_person]
    friends_queue.append('*')
    visited = []

    visited.append(main_person)
    while friends_queue:
        person = friends_queue.popleft()
        if person != '*':
            if not person in visited:
                if person == needed_person:
                    path.append(visited[count_stars])
                    path.append(needed_person)
                    return path
                else:
                    friends_queue += G[person]
                    friends_queue.append('*')
                    visited.append(person)
        else:
            path.append(visited[count_stars])
            count_stars += 1
    return None


def _draw_connection(G, path):  # вспомогательная функ, чтобы добавить позции в новые nodes
    pos = {i: (random.uniform(15, 20), random.uniform(15, 25), random.uniform(0, 20)) for i in range(row_count)}
    for name in G.nodes():  # заполняю nodes  данными
        visited = set()
        if name not in visited:
            visited.add(name)
            if name in list(table['friend']):  # друзья друзей
                if (name in path) and (not G.node.get(name)):
                    data_fr = table.loc[table['friend'] == name]  # ищу все строки с именем
                    ind_fr = data_fr.index[0]  # считаю индекс первой строки с таким именем, для сбора всех данных
                    G.node[name]['pos'] = pos[ind_fr]
        else:
            continue


def draw_connection(G, path, my_ax):
    if not path:  # if path == None
        #########################
        # LEGEND
        fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='y', marker='x')
        my_ax.legend([fake2Dline], ['- no connection'], loc='upper right',
                     title='WARNING:'.format(), numpoints=1, facecolor='#9370DB')
    else:

        _draw_connection(G, path)

        pos = nx.get_node_attributes(G, 'pos')

        for key, value in pos.items():
            if key in path:  # если ключ есть в собранном path
                ######################
                # LEGEND
                fake2Dline = mpl.lines.Line2D([], [], linestyle="none", c='#FF1493', marker='o')
                legend_elements = []
                for f in range(0, len(path)):
                    legend_elements.append(fake2Dline)

                labels = [f'{s}' for s in path]
                my_ax.legend(handles=legend_elements, labels=labels, loc='upper right',
                             title='Path:', numpoints=1, facecolor='#9370DB')
                ##########################
                xi = value[0]
                yi = value[1]
                zi = value[2]

                # Scatter plot      // 20 * G.degree(key)
                my_ax.scatter(xi, yi, zi, c='#FF1493', s=100 * G.degree(key) ** 0.5, edgecolors='k',
                              alpha=0.75)  # change node color
                if key != USER:
                    my_ax.text(xi, yi, zi, key.replace(' ', '\n'), color='#FF1493')  # change label color

            # draw edges
            for i, j in enumerate(G.edges()):
                if (j[0] in path) and (j[1] in path):
                    try:
                        x = np.array((pos[j[0]][0], pos[j[1]][0]))
                        y = np.array((pos[j[0]][1], pos[j[1]][1]))
                        z = np.array((pos[j[0]][2], pos[j[1]][2]))
                    except:
                        continue

                    # Plot the connecting lines
                    my_ax.plot(x, y, z, c='#FF1493', alpha=0.5)

    show_graph(my_ax)  # показывает граф


def find_common_friends_between_friends():
    with open('C:' + os.sep + 'KURSACH' + os.sep + 'my_dict.json', 'r', encoding='utf-8') as f:  # ПЕРЕДЕЛАТЬ
        data = json.loads(f.read())

        arr_sets = []
        arr_interaction = []
        main_user_fr = set()  # set with fr-s of the main user

        for person in data:
            ###### USER ######
            one_dict = data[person]  # доступны 2 словаря
            info = one_dict['general_info']  # словарь с инфой
            name = info['name']
            if name == USER:
                _fr = one_dict['friends_list']
                friends = _fr['friends']
                main_user_fr = set(friends)  # все друзья человека в set
            else:
                _fr_1 = one_dict['friends_list']
                friends_1 = _fr_1['friends']
                fr_set_1 = set(friends_1)
                arr_sets.append(fr_set_1)  # set друзей доюавляется в list

        for i in range(0, len(arr_sets)):
            for j in range(i + 1, len(arr_sets) - 1):
                interaction = arr_sets[i].intersection(arr_sets[j])  # нахожу общих друзей между друзей своих друзей
                if interaction:
                    arr_interaction.append(interaction)  # все пересечения в списке

        famous_friends = {}
        for common in arr_interaction:
            not_fr = list(common.difference(main_user_fr))  # если у юзера нет этих людей в др
            for person in not_fr:
                if person not in famous_friends.keys():
                    famous_friends[person] = 1
                else:
                    famous_friends[person] += 1

        people = []
        for key, value in famous_friends.items():
            if value >= 10 and key != USER:  # САМ ПОЛЬЗОВАТЕЛЬ ЗАДАЕТ СКОЛЬКО VALUE!!!!!!!!!!!!!!!!!
                people.append(key)

        f.close()

        if people:
            return people
        else:
            return None


def draw_common_friends_between_friends(G, common_fr_between_fr, my_ax):
    if not common_fr_between_fr:  # если path == None
        ###########################################
        # LEGEND
        fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='y', marker='x')
        my_ax.legend([fake2Dline], ['- no common friends'], loc='upper right',
                     title='WARNING:'.format(), numpoints=1, facecolor='#9370DB')
    else:
        _draw_connection(G, common_fr_between_fr)

        pos = nx.get_node_attributes(G, 'pos')

        for key, value in pos.items():
            if key in common_fr_between_fr:  # если ключ есть в собранном path
                ###########################################
                # LEGEND
                fake2Dline = mpl.lines.Line2D([], [], linestyle="none", c='#FFA500', marker='o')
                legend_elements = []
                for f in range(0, len(common_fr_between_fr)):
                    legend_elements.append(fake2Dline)

                labels = [f'{s}' for s in common_fr_between_fr]
                my_ax.legend(handles=legend_elements, labels=labels, loc='upper right',
                             title='List:', numpoints=1, facecolor='#9370DB')
                ##########################
                xi = value[0]
                yi = value[1]
                zi = value[2]

                # Scatter plot
                my_ax.scatter(xi, yi, zi, c='#FFA500', s=20 + 20 * G.degree(key), edgecolors='k',
                              alpha=0.75)  # change node color  alpha= прозрачность
                if key != USER:
                    my_ax.text(xi, yi, zi, key.replace(' ', '\n'), color='#FFA500')  # change label color

            # draw edges
            copy_common_fr = common_fr_between_fr.copy()
            for i, j in enumerate(G.edges()):
                if j[1] in copy_common_fr:
                    copy_common_fr.remove(j[1])  # только одно связующее ребро
                    try:
                        x = np.array((pos[j[0]][0], pos[j[1]][0]))
                        y = np.array((pos[j[0]][1], pos[j[1]][1]))
                        z = np.array((pos[j[0]][2], pos[j[1]][2]))
                    except:
                        continue

                    # Plot the connecting lines
                    # my_ax.plot(x, y, z, c='#00FFFF', alpha=0.5)
                    # my_ax.plot(x, y, z, c='#00FF00', alpha=0.5, linewidth=0.3)
                    my_ax.plot(x, y, z, c='#00FF00', alpha=0.3, linewidth=0.3)

    my_ax.view_init(30, 0)  # ?????????????????????????????
    show_graph(my_ax)  # показывает граф


def find_groups():  # доделать
    with open('C:' + os.sep + 'KURSACH' + os.sep + 'my_dict.json', 'r', encoding='utf-8') as f:  # ПЕРЕДЕЛАТЬ
        data = json.loads(f.read())

        arr_sets = []
        main_user_fr = set()

        for person in data:
            ###### USER ######
            one_dict = data[person]  # доступны 2 словаря
            info = one_dict['general_info']  # словарь с инфой
            name = info['name']
            if name == USER:
                _fr = one_dict['friends_list']
                friends = _fr['friends']
                main_user_fr = set(friends)  # все друзья 'главного' человека в set
            else:
                _fr_1 = one_dict['friends_list']
                friends_1 = _fr_1['friends']
                fr_set_1 = set(friends_1)
                arr_sets.append(fr_set_1)  # set друзей добавляется в list

        set_interaction = set()  # ТОЛЬКО ИЗ ДР 1ОГО УРОВНЯ
        for i in range(0, len(arr_sets)):
            for j in range(i + 1, len(arr_sets) - 1):
                interaction = arr_sets[i].intersection(arr_sets[j])  # нахожу общих друзей между друзей своих друзей
                if interaction:
                    for inter in interaction:
                        if inter in main_user_fr:
                            set_interaction.add(inter)

        # отбираем по группам
        study_groups = dict()
        relatives_group = dict()  # ///////////////////////////////////////////////
        for person in data:
            one_dict = data[person]  # доступны 2 словаря
            info = one_dict['general_info']  # словарь с инфой
            name = info['name']

            if name in set_interaction:
                if info.get('study') is not None:
                    study_groups[name] = info['study']
                    # relatives_group[name] =

        arr_with_groups = []  # хранит все собранные групы
        additional_set = set()  # для одной группы
        visited = set()  # для фильтрации посещенных людей
        for key1, value1 in study_groups.items():
            for key2, value2 in study_groups.items():
                if key1 != key2:
                    if (value1 == value2) or (value1.find(value2) != -1):  # если учебы совпадают
                        if key1 not in visited:
                            visited.add(key1)
                            additional_set.add(key1)
                        if key2 not in visited:
                            visited.add(key2)
                            additional_set.add(key2)
            if additional_set:
                additional_set.add('*' + value1)  # добавляю само место учебы(общее для данных людей)
            arr_with_groups.append(additional_set)
            additional_set = set()

        f.close()
        return arr_with_groups


def draw_groups(G, groups, my_ax):
    all_groups = []
    for group in groups:
        if len(group) != 0:
            all_groups.append(group)

    if not all_groups:
        ###########################################
        # LEGEND
        fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='y', marker='x')
        my_ax.legend([fake2Dline], ['- no groups'], loc='upper right',
                     title='WARNING:'.format(), numpoints=1, facecolor='#9370DB')
    else:
        pos = nx.get_node_attributes(G, 'pos')

        colors = ['#FF0000', '#FF69B4', '#FF8C00', '#FFFF00', '#7FFF00', '#00FFFF', '#FFC0CB']
        locations = ['upper right', 'upper left', 'lower left', 'lower right', 'center left', 'center right']

        study_name = ''
        for simple_group in all_groups:  # проход по каждой отдельной группе
            gr = list(simple_group.copy())  # группа без учебного заведения
            for item in simple_group:
                if item.find('*') != -1:
                    study_name = item  # название учебы
                    gr.remove(study_name)

            color = random.choice(colors)  # выбор цвета
            colors.remove(color)

            location = random.choice(locations)  # выбор цвета
            locations.remove(location)

            ###########################################
            # LEGEND
            fake2Dline = mpl.lines.Line2D([], [], linestyle="none", c=color, marker='o')
            legend_elements = []
            for f in range(0, len(gr)):
                legend_elements.append(fake2Dline)

            labels = [f'{s}' for s in gr]
            legend_1 = my_ax.legend(handles=legend_elements, labels=labels, loc=location,
                                    title=f'{study_name.strip("*")}', numpoints=1, facecolor='#9370DB')

            my_ax.add_artist(legend_1)
            ##############################################

            for key, value in pos.items():
                if key in gr:
                    ###########################################
                    # LEGEND
                    fake2Dline = mpl.lines.Line2D([], [], linestyle="none", c=color, marker='o')
                    legend_elements = []
                    for f in range(0, len(gr)):
                        legend_elements.append(fake2Dline)

                    labels = [f'{s}' for s in gr]
                    my_ax.legend(handles=legend_elements, labels=labels, loc=location,
                                 title=f'{study_name}', numpoints=1, facecolor='#9370DB')

                    xi = value[0]
                    yi = value[1]
                    zi = value[2]

                    # Scatter plot
                    my_ax.scatter(xi, yi, zi, c=color, s=20 + 20 * G.degree(key), edgecolors='k',
                                  alpha=0.75)  # change node color  alpha= прозрачность
                    if key != USER:
                        my_ax.text(xi, yi, zi, key.replace(' ', '\n'), color=color)  # change label color

    my_ax.view_init(30, 0)  # ?????????????????????????????
    show_graph(my_ax)  # показывает граф


def main():
    G = create_graph_3D()
    my_ax = draw_graph_3D(G, 0)

    #                  ВЫЗОВЫ
    # find_by_info(G, 'study', 'НИУ ВШЭ', my_ax)  # существующий вуз
    # find_by_info(G, 'study', 'ВШЭ', my_ax)  # существующий вуз + regex
    # find_by_info(G, 'study', 'вшэ', my_ax)  # существующий вуз + regex
    # find_by_info(G, 'study', 'lol', my_ax)  # нет вуза такого
    # find_by_info(G, 'study', 'гимназия', my_ax)  # школа сущ

    # find_by_info(G, 'live in', 'Nizhniy Novgorod', my_ax)  # RE
    # find_by_info(G, 'live in', 'Москва', my_ax)  # RE
    # find_by_info(G, 'live in', 'Nizhniy Novgorod, Russia', my_ax)
    # find_by_info(G, 'live in', 'N N', my_ax)  #  не сущ
    #
    # find_by_info(G, 'b-day', 'lol', my_ax)  #  не сущ
    # find_by_info(G, 'b-day', '17 ноября 1995 г.',my_ax)  # сущ ВСЕ
    # find_by_info(G, 'b-day', 'Ноябрь', my_ax)  # месяц НОЯБРЬ
    # find_by_info(G, 'b-day', '17', my_ax)  # число
    # find_by_info(G, 'b-day', '1995', my_ax)  # год

    #                      FIND PATH
    # path = find_connection(G, 'Полина Ожиганова', 'Katerina Tyulina') # path exists
    # path = find_connection(G, 'Полина Ожиганова', 'Олег Паканин')  # path exists
    # path = find_connection(G, 'Полина Ожиганова', 'Гарри Поттер')  # path DOESN'T exist

    #                      DRAW PATH
    # draw_connection(G, path, my_ax)

    #                      FIND COMMON FRIENDS
    # common_fr_between_fr = find_common_friends_between_friends()

    #                      DRAW COMMON FRIENDS
    # draw_common_friends_between_friends(G, common_fr_between_fr, my_ax)

    #                      FIND GROUPS
    # groups = find_groups() # ОСТАВИТЬ???

    #                      DRAW GROUPS
    # draw_groups(G, groups, my_ax)


if __name__ == '__main__':
    main()

