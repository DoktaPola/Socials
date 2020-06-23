import json
import os
import random
import re
import time
from collections import deque
from os.path import abspath

import matplotlib.pyplot as plt, mpld3
import networkx as nx
import pandas as pd
from pyvis.network import Network

################## GLOBAL ##############################
plt.style.use('dark_background')  # темный фон
font_style = {'fontname': 'Bookman Old Style'}

net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

# file_name = 'Friends_DF.csv'
file_name = 'File_CSV.csv'
f = os.path.abspath(file_name)
table = pd.read_csv(f)

row_count = len(table['name'])  # сколько строчек
TIME_LIMIT = 60
USER = table['name'][0]

if row_count > 1500:
    net.force_atlas_2based(gravity=-1000)
else:
    net.barnes_hut()  # растановка nodes

def show_graph():
    net.show("facebook_net.html")
    plt.axis('off')  # hide the axes
    mpld3.show()


def create_graph():
    sources = table['name']
    targets = table['friend']
    edge_data = zip(sources, targets)

    for e in edge_data:
        src = e[0]
        dst = e[1]

        net.add_node(src, src, title=src)
        net.add_node(dst, dst, title=dst)
        net.add_edge(src, dst)

    neighbor_map = net.get_adj_list()

    for node in net.nodes:
        visited = set()

        name = node.get('title')
        if name not in visited:

            if name == USER:  # the main user
                name = node.get('label')

                node['color'] = '#EE82EE'
                node['size'] = 100
                node['shape'] = 'diamond'

            visited.add(name)

            if name in list(table['name']):  # проверяю есть ли имя в таблице в столбце 'name'
                data = table.loc[table['name'] == name]  # ищу все строки с именем
                ind = data.index[0]  # считаю индекс первой строки с таким именем, для сбора всех данных

                node['study'] = data.study[ind]
                node['live in'] = data['live in'][ind]
                node['b-day'] = data['b-day'][ind]
                node['e-mail'] = data['e-mail'][ind]
                ###################################
                label = ['***INFO***']

                if data.study[ind] != '-':
                    study = 'Study: ' + str(data.study[ind])
                    label.append(study)
                if data['live in'][ind] != '-':
                    live_in = 'Live in: ' + str(data['live in'][ind])
                    label.append(live_in)
                if data.links[ind] != '-':
                    links = 'Link: ' + str(data.links[ind])
                    label.append(links)
                if data['b-day'][ind] != '-':
                    b_day = 'B-day: ' + str(data['b-day'][ind])
                    label.append(b_day)
                if data['e-mail'][ind] != '-':
                    e_mail = 'E-mail: ' + str(data['e-mail'][ind])
                    label.append(e_mail)

                if len(label) > 1:
                    node["title"] += "\n" + "<br>" + "<br>".join(label)

                s = len(neighbor_map[node["id"]])  # выделяю, кто имеет больше друзей, чтобы увеличить размер node
                max_s = max([len(neighbor_map[node["id"]]) for node in net.nodes])  # the biggest amount of friends

                if s < (max_s / 2):
                    node['size'] = s + 30
                else:
                    node['size'] = s + 40
        else:
            continue
    # LEGEND
    plt.text(0.05, 0.8, 'Hello!', color='yellow', size=20, weight='normal', **font_style)
    plt.text(0.05, 0.75, 'This is your Facebook network!', color='white', size=16, weight='light', **font_style)

###################################################################
#                      Network Analysis
###################################################################


def get_key(dictionary: dict, value):  # return key
    for k, v in dictionary.items():
        if v == value:
            finale = k
            dictionary.pop(k)
            return finale


def work_study(attr, info):
    study = []
    attr2 = attr.copy()  # работаю с копией словаря, чтобы удалять элементы
    for a in attr.values():  # try to find key
        info_lower = info.lower()
        a_lower = str(a).lower()
        if re.search(r"[а-яА-Яa-zA-Z]*\s?%s\s?[а-яА-Яa-zA-Z]*" % info_lower, a_lower):
            study.append(get_key(attr2, a))

    ##############################
    if not study:  # if study doesn't exist
        #########################################
        # LEGEND
        plt.text(0.05, 0.94, 'Study: {}'.format(info), color='yellow', size=14, weight='normal', **font_style)
        plt.text(0.05, 0.8, '! not found !', color='white', size=14, weight='light', **font_style)
        ###############################3
        show_graph()
        return
    for node in net.nodes:
        name = node.get('label')
        if name in study:
            node['color'] = '#00FF00'
            node['size'] = 150

    for edge in net.edges:
        name1 = edge.get('from')
        name2 = edge.get('to')
        if name1 in study or name2 in study:
            edge['color'] = '#1E90FF'

    #########################################
    # LEGEND
    fig, ax = plt.subplots()
    ax = fig.add_subplot()

    plt.text(0.05, 0.95, 'Study: {}'.format(info), color='#00FF00', size=14, weight='normal', **font_style)

    y = 0.9
    for s in study:
        x = 0.05
        circle = plt.Circle((x, y), radius=0.01, color='#00FF00')
        ax.add_patch(circle)

        plt.text(x + 0.07, y - 0.01, s, color='white', size=10, weight='light', **font_style)

        ax.set_aspect('equal')
        y -= 0.04
    ###########################
    show_graph()


def work_live_in(attr, info):
    live_in = []
    attr2 = attr.copy()  # работаю с копией словаря, чтобы удалять элементы
    for a in attr.values():  # try to find key
        info_lower = info.lower()
        a_lower = str(a).lower()
        if re.search(r"[а-яА-Яa-zA-Z]*\s?%s\s?[а-яА-Яa-zA-Z]*" % info_lower, a_lower):
            live_in.append(get_key(attr2, a))

    if not live_in:  # if live_in doesn't exist
        #########################################
        # LEGEND
        plt.text(0.05, 0.94, 'Live in: {}'.format(info), color='yellow', size=14, weight='normal', **font_style)
        plt.text(0.05, 0.8, '! not found !', color='white', size=14, weight='light', **font_style)
        ###############################3
        show_graph()
        return

    for node in net.nodes:
        name = node.get('label')
        if name in live_in:
            node['color'] = '#FFFF00'
            node['size'] = 150

    for edge in net.edges:
        name1 = edge.get('from')
        name2 = edge.get('to')
        if name1 in live_in or name2 in live_in:
            edge['color'] = '#1E90FF'
    #########################################
    # LEGEND
    fig, ax = plt.subplots()
    ax = fig.add_subplot()
    plt.axis('off')  ###########

    plt.text(0.05, 0.95, 'Live in: {}'.format(info), color='#FFFF00', size=14, weight='normal', **font_style)

    y = 0.9
    for s in live_in:
        x = 0.05
        circle = plt.Circle((x, y), radius=0.01, color='#FFFF00')
        ax.add_patch(circle)

        plt.text(x + 0.07, y - 0.01, s, color='white', size=10, weight='light', **font_style)

        ax.set_aspect('equal')
        y -= 0.04
    ###############################
    show_graph()  # показывает граф


def work_b_day(attr, info):
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

    #################################
    if not b_day:  # if live_in doesn't exist
        #########################################
        # LEGEND
        plt.text(0.05, 0.94, 'B-day: {}'.format(info), color='yellow', size=14, weight='normal', **font_style)
        plt.text(0.05, 0.8, '! not found !', color='white', size=14, weight='light', **font_style)
        ###############################3
        show_graph()
        return

    for node in net.nodes:
        name = node.get('label')
        if name in b_day:
            node['color'] = '#FF8C00'
            node['size'] = 150

    for edge in net.edges:
        name1 = edge.get('from')
        name2 = edge.get('to')
        if name1 in b_day or name2 in b_day:
            edge['color'] = '#1E90FF'
    #########################################
    # LEGEND
    fig, ax = plt.subplots()
    ax = fig.add_subplot()

    plt.text(0.05, 0.95, 'B-day: {}'.format(info), color='#FF8C00', size=14, weight='normal', **font_style)

    y = 0.9
    for s in b_day:
        x = 0.05
        circle = plt.Circle((x, y), radius=0.01, color='#FF8C00')
        ax.add_patch(circle)

        plt.text(x + 0.07, y - 0.01, s, color='white', size=10, weight='light', **font_style)

        ax.set_aspect('equal')
        y -= 0.04
    ###############################3
    show_graph()  # показывает граф


def find_by_info(column, info):  # нахожу в графе инфу по заданной колонке
    attr = dict()

    if column == 'study':
        for node in net.nodes:
            study = node.get('study')
            name = node.get('label')
            attr[name] = study
        work_study(attr, info)

    if column == 'live in':
        for node in net.nodes:
            live = node.get('live in')
            name = node.get('label')
            attr[name] = live
        work_live_in(attr, info)

    if column == 'b-day':
        for node in net.nodes:
            b_day = node.get('b-day')
            name = node.get('label')
            attr[name] = b_day
        work_b_day(attr, info)


def _create_graph():
    FB = nx.from_pandas_edgelist(table, source='name', target='friend')  # создаю граф с ребрами без атрибутов

    for name in FB.nodes():  # fill data in nodes
        visited = set()

        if name not in visited:
            visited.add(name)

            if name in list(table['name']):  # проверяю есть ли имя в таблице в столбце 'name'
                data = table.loc[table['name'] == name]  # ищу все строки с именем
                ind = data.index[0]  # считаю индекс первой строки с таким именем, для сбора всех данных

                FB.nodes[name]['id'] = data.id[ind]
                FB.nodes[name]['study'] = data.study[ind]
                FB.nodes[name]['live in'] = data['live in'][ind]
                FB.nodes[name]['links'] = data.links[ind]
                FB.nodes[name]['b-day'] = data['b-day'][ind]
                FB.nodes[name]['e-mail'] = data['e-mail'][ind]
        else:
            continue
    return FB


def find_connection(G, begin, stop, q):  # bfs
    start_time = time.time()

    t_path = [begin]
    q.append(t_path)

    while len(q) != 0:
        if time.time() - start_time > TIME_LIMIT:
            return None
        temp_path = q.popleft()
        last_node = temp_path[len(temp_path) - 1]
        if last_node == stop:
            return temp_path
        for node in G[last_node]:
            if node not in temp_path:
                new_path = []
                new_path = temp_path + [node]
                q.append(new_path)
    return None


def draw_connection(path):
    if not path:  # if path == None
        #########################################
        # LEGEND
        plt.text(0.05, 0.94, 'Path', color='yellow', size=14, weight='normal', **font_style)
        plt.text(0.05, 0.8, '! not found !', color='white', size=14, weight='light', **font_style)
        ###############################3
        show_graph()
        return
    else:
        for node in net.nodes:
            name = node.get('label')
            if name in path:
                node['color'] = '#FF1493'
                node['size'] = 150

        for edge in net.edges:
            name1 = edge.get('from')
            name2 = edge.get('to')
            if name1 in path and name2 in path:
                edge['color'] = '#FF1493'
                edge['width'] = 50
    #########################################
    # LEGEND
    fig, ax = plt.subplots()
    ax = fig.add_subplot()
    plt.axis('off')  ###########

    plt.text(0.05, 0.95, 'Path', color='#FF1493', size=14, weight='normal', **font_style)

    y = 0.9
    for s in path:
        x = 0.05
        circle = plt.Circle((x, y), radius=0.01, color='#FF1493')
        ax.add_patch(circle)

        plt.text(x + 0.07, y - 0.01, s, color='white', size=11, weight='light', **font_style)

        ax.set_aspect('equal')
        y -= 0.04
    ###############################
    show_graph()  # показывает граф


def find_common_friends_between_friends():
    file_name = 'friends.json'
    with open(os.path.abspath(file_name), 'r', encoding='utf-8') as f:
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
                main_user_fr = set(friends)  # все друзья главн пользователя в set
            else:
                _fr_1 = one_dict['friends_list']
                friends_1 = _fr_1['friends']
                if friends_1:
                    fr_set_1 = set(friends_1)
                    arr_sets.append(fr_set_1)  # set друзей добавляется в list

        for i in range(0, len(arr_sets)):
            for j in range(i + 1, len(arr_sets) - 1):
                interaction = arr_sets[i].intersection(arr_sets[j])  # нахожу общих друзей между друзей друзей гл. юзера
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


def draw_common_friends_between_friends(common_fr_between_fr):
    neighbor_map = net.get_adj_list()

    if not common_fr_between_fr:  # если path == None
        #########################################
        # LEGEND
        plt.text(0.05, 0.94, 'Common friends', color='yellow', size=14, weight='normal', **font_style)
        plt.text(0.05, 0.8, '! not found !', color='white', size=14, weight='light', **font_style)
        ###############################3
        show_graph()
        return
    else:
        for node in net.nodes:
            name = node.get('label')
            if name == USER:  # выделяем главного пользователя
                node['color'] = '#EE82EE'
                node['size'] = 100

            if name in common_fr_between_fr:
                node['color'] = '#FFA500'
                node['size'] = 150

                node["title"] += '\n' + "Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])

        for edge in net.edges:
            name1 = edge.get('from')
            name2 = edge.get('to')
            if name1 == USER or name2 == USER:
                edge['color'] = '#1E90FF'
    #########################################
    # LEGEND
    fig, ax = plt.subplots()
    ax = fig.add_subplot()

    plt.text(0.05, 0.95, 'You can be friends with:', color='#FFA500', size=14, weight='normal', **font_style)

    y = 0.9
    for s in common_fr_between_fr:
        x = 0.05
        circle = plt.Circle((x, y), radius=0.01, color='#FFA500')

        ax.add_patch(circle)

        plt.text(x + 0.07, y - 0.01, s, color='white', size=10, weight='light', **font_style)

        ax.set_aspect('equal')
        y -= 0.04
    ###############################3
    show_graph()  # показывает граф


def find_groups():
    file_name = 'friends.json'
    with open(os.path.abspath(file_name), 'r', encoding='utf-8') as f:
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
                if friends_1:
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
        for person in data:
            one_dict = data[person]  # доступны 2 словаря
            info = one_dict['general_info']  # словарь с инфой
            name = info['name']

            if name in set_interaction:
                if info.get('study') is not None:
                    study_groups[name] = info['study']

        arr_with_groups = []  # хранит все собранные группы
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
                additional_set.add('*' + value1)  # добавляю само место учебы(общее для данной группы)
            arr_with_groups.append(additional_set)
            additional_set = set()

        f.close()
        return arr_with_groups


def draw_groups(groups):
    all_groups = []
    for group in groups:
        if len(group) != 0:
            all_groups.append(group)

    if not all_groups:
        #########################################
        # LEGEND
        plt.text(0.05, 0.94, 'Groups', color='yellow', size=14, weight='normal', **font_style)
        plt.text(0.05, 0.8, '! not found !', color='white', size=14, weight='light', **font_style)
        ###############################3
        show_graph()
        return
    else:
        #########################################
        # LEGEND
        fig, ax = plt.subplots()
        ax = fig.add_subplot()

        plt.text(0.05, 0.95, 'Groups', color='#1E90FF', size=14, weight='normal', **font_style)

        y = 0.9
        x = 0.05
        ###############################3

        colors = ['#FF0000', '#FF69B4', '#FF8C00', '#FFFF00', '#7FFF00', '#00FFFF', '#FFC0CB']
        study_name = ''
        for simple_group in all_groups:  # проход по каждой отдельной группе
            gr = list(simple_group.copy())  # группа без учебного заведения
            for item in simple_group:
                if item.find('*') != -1:
                    study_name = item  # название учебы
                    gr.remove(study_name)

            color = random.choice(colors)  # выбор цвета
            colors.remove(color)
            ########################
            #    Legend
            circle = plt.Circle((x, y), radius=0.02, color=color)
            ax.add_patch(circle)
            plt.text(x + 0.07, y - 0.01, study_name.strip("*"), color='white', size=11, weight='light', **font_style)
            ax.set_aspect('equal')
            y -= 0.05
            #########################
            for node in net.nodes:
                name = node.get('label')
                if name in gr:
                    node['color'] = color
                    node['size'] = 100

            for edge in net.edges:
                name1 = edge.get('from')
                name2 = edge.get('to')
                if name1 == USER or name2 == USER:
                    edge['color'] = '#1E90FF'
    show_graph()  # показывает граф


def main():
    create_graph()
    # net.show("facebook_net.html")
    # show_graph()

    #                  ВЫЗОВЫ
    # find_by_info('study', 'НИУ ВШЭ')  # существующий вуз
    # find_by_info('study', 'ВШЭ')  # существующий вуз + regex
    # find_by_info('study', 'вшэ')  # существующий вуз + regex
    # find_by_info('study', 'lol')  # нет вуза такого
    # find_by_info('study', 'гимназия')  # школа сущ

    # find_by_info('live in', 'Nizhniy Novgorod')  # RE
    # find_by_info('live in', 'Москва')  # RE
    # find_by_info('live in', 'Nizhniy Novgorod, Russia')
    # find_by_info('live in', 'N N')  #  не сущ
    #
    # find_by_info('b-day', 'lol')  #  не сущ
    # find_by_info('b-day', '17 ноября 1995 г.')  # сущ ВСЕ
    # find_by_info('b-day', 'Ноябрь')  # месяц НОЯБРЬ
    # find_by_info('b-day', '17')  # число
    # find_by_info('b-day', '1995')  # год

    #                      FIND PATH
    friends_queue = deque()  # !!!!
    FB = _create_graph()   # !!!!

    # path = find_connection(FB, 'Полина Ожиганова', 'Katerina Tyulina', friends_queue)  # path exists
    # path = find_connection(FB, 'Полина Ожиганова', 'Олег Паканин', friends_queue)  # path exists
    # path = find_connection(FB, 'Полина Ожиганова', 'Гарри Поттер', friends_queue)  # path DOESN'T exist
    path = find_connection(FB, 'Tanya Termeneva', 'Елена Рогожина', friends_queue)  # path exists
    #                      DRAW PATH
    draw_connection(path)

    #                      FIND COMMON FRIENDS
    #common_fr_between_fr = find_common_friends_between_friends()

    #                      DRAW COMMON FRIENDS
    #draw_common_friends_between_friends(common_fr_between_fr)

    #                      FIND GROUPS
    #groups = find_groups()

    #                      DRAW GROUPS
    #draw_groups(groups)


if __name__ == '__main__':
    main()
