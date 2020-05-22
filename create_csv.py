import pandas as pd
import numpy as np
import json
from openpyxl import Workbook

with open('POLA.json', 'r', encoding='utf-8') as f:
    data = json.loads(f.read())

    df = None
    all_dicts = []
    for person in data:
        one_dict = data[person]  # доступны 2 словаря
        info = one_dict['general_info']  # словарь с инфой
        _fr = one_dict['friends_list']
        friends = _fr['friends']

        id = person
        name = info['name']

        if info.get('study'):
            study = info['study']
        else:
            study = '-'

        if info.get('live_in'):
            live_in = info['live_in']
        else:
            live_in = '-'

        if info.get('links'):
            links = info['links']
        else:
            links = '-'

        if info.get('b-day'):
            b_day = info['b-day']
        else:
            b_day = '-'

        if info.get('email'):
            email = info['email']
        else:
            email = '-'

        if info.get('some_info'):
            some_info = info['some_info']
        else:
            some_info = '-'

        for friend in friends:
            d = {'id': person, 'name': name, 'study': study, 'live in': live_in,
                 'links': links, 'b-day': b_day, 'e-mail': email,
                 'some info': some_info, 'friend': friend}

            all_dicts.append(d)

    df = pd.DataFrame(all_dicts)
    # print(df)

    # df.to_excel(r'C:\KURSACH\TABLE.xlsx', index=False)
    # read_file = pd.read_excel(r'C:\KURSACH\TABLE.xlsx')
    # read_file.to_csv(r'File_CSV.csv', index=None, header=True)
    df.to_csv(r'POLA_CSV.csv', index=None, header=True)