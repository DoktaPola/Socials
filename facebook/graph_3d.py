import json
import os
import re
import time
from collections import deque

import matplotlib as mpl
import random

from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import warnings
import queue
import networkx as nx
import pandas as pd
import pylab
from mpl_toolkits.mplot3d import proj3d

warnings.filterwarnings('ignore')
csfont = {'fontname': 'Comic Sans MS'}

################## GLOBE ##############################
labels = []
table = pd.read_csv('C:\KURSACH\File_CSV.csv')
row_count = len(table['name'])  # сколько строчек

# USER = 'Полина Ожиганова'  # СДЕЛАТЬ НОРМАЛЬНО!!!!!!!!!!!!!!!!!!!!!!!!!!!
USER = table['name'][0]


def generate_random_3Dgraph():
    FB = nx.from_pandas_edgelist(table, source='name', target='friend')  # создаю граф с ребрами без атрибутов
    pos = {i: (random.uniform(15, 20), random.uniform(15, 25), random.uniform(0, 20)) for i in range(row_count)}

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
            # elif name in list(table['friend']):  # друзья друзей
            #     if FB.degree(name) > 1:  # add only people whose degree is bigger then 1
            #         data_fr = table.loc[table['friend'] == name]  # ищу все строки с именем
            #         ind_fr = data_fr.index[0]  # считаю индекс первой строки с таким именем, для сбора всех данных
            #         FB.node[name]['pos'] = pos[ind_fr]
        else:
            continue
    return FB


def network_plot_3D(G, angle, save=False):
    # Get node positions
    pos = nx.get_node_attributes(G, 'pos')

    # add labels
    for k in G.nodes():
        l = k.replace(' ', '\n')
        labels.append(l)

    # Get the maximum number of edges adjacent to a single node
    edge_max = max([G.degree(node) for node in G.nodes()])
    # Define color range proportional to number of edges adjacent to a single node
    colors = [plt.cm.plasma(G.degree(node) / edge_max) for node in G.nodes()]

    # 3D network plot
    with plt.style.context(('ggplot')):

        # fig = plt.figure(figsize=(10, 7))
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
            # ax.scatter(xi, yi, zi, c=colors[key], s=20 + 20 * G.degree(key), edgecolors='k', alpha=0.7)
            # ax.text(xi, yi, zi, labels[counter], color='#f7e6ff') # ТОЛЬКО ДЛЯ ТЕХ, У КОГО МНОГО ДРУЗЕЙ
            # counter += 1

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
    # ax.set_axis_off()
    # if save is not False:
    #     plt.savefig(':\scratch\\data\"+str(angle).zfill(3)+".png')
    #     plt.close('all')
    # else:
    #     # get black background
    #     plt.gca().patch.set_facecolor('black')
    #     ax.w_xaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
    #     ax.w_yaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
    #     ax.w_zaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
    #     plt.show()
    return ax


####################################################################


def get_key(d, value):  # возвращает ключ по значению
    for k, v in d.items():
        if v == value:
            finale = k
            d.pop(k)
            return finale


def work_study(G, attr, info, my_ax):
    pos = nx.get_node_attributes(G, 'pos')

    study = []
    attr2 = attr.copy()  # работаю с копией словаря, чтобы удалять элементы
    for a in attr.values():  # try to find key   ОРГАНИЗОВАТЬ БЫСТРЫЙ ПОИСК
        info_lower = info.lower()
        a_lower = str(a).lower()
        if re.search(r"[а-яА-Яa-zA-Z]*\s?%s\s?[а-яА-Яa-zA-Z]*" % info_lower, a_lower):
            study.append(get_key(attr2, a))

    for key, value in pos.items():
        if not study:  # если study не существует
            ###########################################
            # LEGEND
            fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='y', marker='x')
            my_ax.legend([fake2Dline], ['- no such place'], loc='upper right',
                         title='WARNING:'.format(info), numpoints=1, facecolor='#9370DB')
            ##########################
            # my_ax.text2D(0.05, 0.95,
            #              'WARNING:',
            #              color='yellow',
            #              size=18,
            #              weight='normal',  # ////////////////////////////////////////////////////////////
            #              **csfont,
            #              transform=my_ax.transAxes)
            #
            # my_ax.text2D(0.05, 0.92,
            #              '- no such place',
            #              color='white',
            #              size=14,
            #              weight='light',  # ////////////////////////////////////////////////////////////
            #              **csfont,
            #              transform=my_ax.transAxes)
            break
        if key in study:  # если ключ есть в собранном study [ ]
            ###########################################
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
                          alpha=0.7)  # change node color
            if key != USER:
                my_ax.text(xi, yi, zi, key.replace(' ', '\n'), color='#00BFFF')  # change label color

    # if study:
    #     my_ax.text2D(0.05, 0.95,
    #                  'Study: {}'.format(info),
    #                  color='#00BFFF',
    #                  size=18,
    #                  weight='normal', #////////////////////////////////////////////////////////////
    #                  **csfont,
    #                  transform=my_ax.transAxes)
    #     x = 0.05
    #     y = 0.92
    #     for s in study:
    #         my_ax.text2D(x, y, s,
    #                      color='white',
    #                      size=14,
    #                      weight='light', #////////////////////////////////////////////////////////////
    #                      **csfont,
    #                      transform=my_ax.transAxes)
    #         y -= 0.03

    # Hide the axes
    my_ax.set_axis_off()

    # get black background
    plt.gca().patch.set_facecolor('black')
    my_ax.w_xaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
    my_ax.w_yaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
    my_ax.w_zaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
    plt.show()


def work_live_in(G, attr, info, my_ax):
    pos = nx.get_node_attributes(G, 'pos')

    live_in = []
    attr2 = attr.copy()  # работаю с копией словаря, чтобы удалять элементы
    for a in attr.values():  # try to find key   ОРГАНИЗОВАТЬ БЫСТРЫЙ ПОИСК
        info_lower = info.lower()
        a_lower = str(a).lower()
        if re.search(r"[а-яА-Яa-zA-Z]*\s?%s\s?[а-яА-Яa-zA-Z]*" % info_lower, a_lower):
            live_in.append(get_key(attr2, a))

    for key, value in pos.items():
        if not live_in:  # если live_in не существует
            ###########################################
            # LEGEND
            fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='y', marker='x')
            my_ax.legend([fake2Dline], ['- no information'], loc='upper right',
                         title='WARNING:'.format(info), numpoints=1, facecolor='#9370DB')

            break
        if key in live_in:  # если ключ есть в собранном live_in
            ###########################################
            # LEGEND
            fake2Dline = mpl.lines.Line2D([], [], linestyle="none", c='#FFFF00', marker='o')
            legend_elements = []
            for f in range(0, len(live_in)):
                legend_elements.append(fake2Dline)

            labels = [f'{s}' for s in live_in]
            my_ax.legend(handles=legend_elements, labels=labels, loc='upper left',
                         title='Live in: {}'.format(info), numpoints=1, facecolor='#9370DB')
            ##########################
            xi = value[0]
            yi = value[1]
            zi = value[2]

            # Scatter plot
            my_ax.scatter(xi, yi, zi, c='#FFFF00', s=20 + 20 * G.degree(key), edgecolors='k',
                          alpha=0.7)  # change node color
            if key != USER:
                my_ax.text(xi, yi, zi, key.replace(' ', '\n'), color='#FFFF00')  # change label color

    # Hide the axes
    my_ax.set_axis_off()

    # get black background
    plt.gca().patch.set_facecolor('black')
    my_ax.w_xaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
    my_ax.w_yaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
    my_ax.w_zaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
    plt.show()


def work_b_day(G, attr, info, my_ax):
    pos = nx.get_node_attributes(G, 'pos')

    b_day = []
    attr2 = attr.copy()  # работаю с копией словаря, чтобы удалять элементы
    for a in attr.values():  # try to find key   ОРГАНИЗОВАТЬ БЫСТРЫЙ ПОИСК
        # info_lower = None
        if info.isalpha():
            _inf = info[:-1]
            info_lower = _inf.lower()
        else:
            info_lower = info.lower()
        a_lower = str(a).lower()

        if re.search(r"[а-яА-Яa-zA-Z0-9]*\s?%s\s?[а-яА-Яa-zA-Z0-9]*" % info_lower, a_lower):
            b_day.append(get_key(attr2, a))

    for key, value in pos.items():
        if not b_day:  # если b_day не существует
            ###########################################
            # LEGEND
            fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='y', marker='x')
            my_ax.legend([fake2Dline], ['- no information'], loc='upper right',
                         title='WARNING:'.format(info), numpoints=1, facecolor='#9370DB')

            break
        if key in b_day:  # если ключ есть в собранном live_in
            ###########################################
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
                          alpha=0.7)  # change node color
            if key != USER:
                my_ax.text(xi, yi, zi, key.replace(' ', '\n'), color='#FF8C00')  # change label color

        # Hide the axes
    my_ax.set_axis_off()

    # get black background
    plt.gca().patch.set_facecolor('black')
    my_ax.w_xaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
    my_ax.w_yaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
    my_ax.w_zaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
    plt.show()


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
    return None  #########################


def _draw_connection(G, path):
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
    if not path:  # если path == None
        ###########################################
        # LEGEND
        fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='y', marker='x')
        my_ax.legend([fake2Dline], ['- no connection'], loc='upper right',
                     title='WARNING:'.format(), numpoints=1, facecolor='#9370DB')
    else:

        _draw_connection(G, path)

        pos = nx.get_node_attributes(G, 'pos')

        for key, value in pos.items():
            if key in path:  # если ключ есть в собранном path
                ###########################################
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

                # Scatter plot
                my_ax.scatter(xi, yi, zi, c='#FF1493', s=20 + 20 * G.degree(key), edgecolors='k',
                              alpha=0.7)  # change node color
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
        # Hide the axes
    my_ax.set_axis_off()

    # get black background
    plt.gca().patch.set_facecolor('black')
    my_ax.w_xaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
    my_ax.w_yaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
    my_ax.w_zaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
    plt.show()


# def find_common_friends_between_friends():
#     with open('C:' + os.sep + 'KURSACH' + os.sep + 'my_dict.json', 'r', encoding='utf-8') as f:  # ПЕРЕДЕЛАТЬ
#         data = json.loads(f.read())
#
#         arr_sets = []
#         ############ SETS ##############
#         main_user_fr = set()  # set with fr-s of the main user
#         interaction_set = set()
#
#         for person in data:
#             ###### USER ######
#             one_dict = data[person]  # доступны 2 словаря
#             info = one_dict['general_info']  # словарь с инфой
#             name = info['name']
#             if name == USER:
#                 _fr = one_dict['friends_list']
#                 friends = _fr['friends']
#                 main_user_fr = set(friends)
#             else:
#                 _fr_1 = one_dict['friends_list']
#                 friends_1 = _fr_1['friends']
#                 fr_set_1 = set(friends_1)
#                 arr_sets.append(fr_set_1)
#
#         for i in range(0, len(arr_sets)):
#             for j in range(i + 1, len(arr_sets) - 1):
#                 interaction = arr_sets[i].intersection(arr_sets[j])
#                 if interaction:
#                     while interaction:
#                         user_name = interaction.pop()
#                         interaction_set.add(user_name)
#
#         people = list(interaction_set.difference(main_user_fr))
#         if people:
#             return people
#         else:
#             return None

def find_common_friends_between_friends():
    with open('C:' + os.sep + 'KURSACH' + os.sep + 'my_dict.json', 'r', encoding='utf-8') as f:  # ПЕРЕДЕЛАТЬ
        data = json.loads(f.read())

        arr_sets = []
        arr_interaction = []
        ############ SETS ##############
        main_user_fr = set()  # set with fr-s of the main user
        interaction_set = set()

        for person in data:
            ###### USER ######
            one_dict = data[person]  # доступны 2 словаря
            info = one_dict['general_info']  # словарь с инфой
            name = info['name']
            if name == USER:
                _fr = one_dict['friends_list']
                friends = _fr['friends']
                main_user_fr = set(friends) # все друзья человека в set
            else:
                _fr_1 = one_dict['friends_list']
                friends_1 = _fr_1['friends']
                fr_set_1 = set(friends_1)
                arr_sets.append(fr_set_1) # set друзей доюавляется в list

        for i in range(0, len(arr_sets)):
            for j in range(i + 1, len(arr_sets) - 1):
                interaction = arr_sets[i].intersection(arr_sets[j]) # нахожу общих друзей между друзей своих друзей
                if interaction:
                    arr_interaction.append(interaction) # все пересечения в списке

        famous_friends = {}
        for common in arr_interaction:
            not_fr = list(common.difference(main_user_fr)) # если у юзера нет этих людей в др
            for person in not_fr:
                if person not in famous_friends.keys():
                    famous_friends[person] = 1
                    # famous_friends.append(fr_count)
                else:
                    famous_friends[person] += 1

        people = []
        for key, value in famous_friends.items():
            if value >= 10 and key != USER:  # САМ ПОЛЬЗОВАТЕЛЬ ЗАДАЕТ СКОЛЬКО VALUE!!!!!!!!!!!!!!!!!
                people.append(key)

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
                    fake2Dline = mpl.lines.Line2D([], [], linestyle="none", c='#00FFFF', marker='o')
                    legend_elements = []
                    for f in range(0, len(common_fr_between_fr)):
                        legend_elements.append(fake2Dline)

                    labels = [f'{s}' for s in common_fr_between_fr]
                    my_ax.legend(handles=legend_elements, labels=labels, loc='upper right',
                                 title='Path:', numpoints=1, facecolor='#9370DB')
                    ##########################
                    xi = value[0]
                    yi = value[1]
                    zi = value[2]

                    # Scatter plot
                    my_ax.scatter(xi, yi, zi, c='#00FFFF', s=20 + 20 * G.degree(key), edgecolors='k',
                                  alpha=0.7)  # change node color
                    if key != USER:
                        my_ax.text(xi, yi, zi, key.replace(' ', '\n'), color='#00FFFF')  # change label color

                # draw edges
                copy_common_fr = common_fr_between_fr.copy()
                for i, j in enumerate(G.edges()):
                    if j[1] in copy_common_fr:
                        copy_common_fr.remove(j[1])
                        try:
                            x = np.array((pos[j[0]][0], pos[j[1]][0]))
                            y = np.array((pos[j[0]][1], pos[j[1]][1]))
                            z = np.array((pos[j[0]][2], pos[j[1]][2]))
                        except:
                            continue

                        # Plot the connecting lines
                        # my_ax.plot(x, y, z, c='#00FFFF', alpha=0.5)
                        my_ax.plot(x, y, z, c='#00FF00', alpha=0.5)

        my_ax.view_init(30, 0)   # ?????????????????????????????
            # Hide the axes
        my_ax.set_axis_off()

        # get black background
        plt.gca().patch.set_facecolor('black')
        my_ax.w_xaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
        my_ax.w_yaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
        my_ax.w_zaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
        plt.show()


def main():
    G = generate_random_3Dgraph()
    my_ax = network_plot_3D(G, 0, save=False)

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
    common_fr_between_fr = find_common_friends_between_friends()
    # print(find_common_friends_between_friends())

    #                      DRAW COMMON FRIENDS
    draw_common_friends_between_friends(G, common_fr_between_fr, my_ax)

if __name__ == '__main__':
    main()
