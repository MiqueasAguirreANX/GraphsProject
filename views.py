"""
Graphs will measure combined data points for all the data from the repos of the 16 chosen projects

Presented as a line graph without specific project markers:
How many developers there are across all projects
Average contribution by developers per month in days
Frequent vs infrequent developers
For frequent vs infrequent contributions:
if a Deve contributed code more than 10 days of the month they're frequent and less than 10 days they're infrequent.

Presented as a combination of bar graphs, line graphs and scatter plots with specific project markers:
Number of active monthly developers on the projects
Frequent developers on the projects
Infrequent developers on the projects
How many developers commit each month
Rank from largest to smallest projects by number of developers
Rank from most active to least active by number of commits
Growth from first commit
Which projects gained developers
Which projects stayed the same
Which projects lost developers
Sizes of the teams
"""
from collections import Counter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

ORGANIZATIONS = {
    'omgnetwork': {},
    'maticnetwork': {},
    'cryptoeconomicslab': {},  # obtuve error 0 1 /gazelle
    'perun-network': {},
    'raiden-network': {},  # obtuve error 20
    'connext': {},
    'AztecProtocol': {},
    'matter-labs': {},  # obtuve error 0 1 /zksync
    'LoopringSecondary': {},  # obtuve error 0 1 /protocol
    'starkware-libs': {},  # obtuve error 0 1
    'fuellabs': {},
    'ethereum-optimism': {},  # obtuve error 29
    'OffchainLabs': {},  # obtuve error 0 1 /arbitrum
    'celer-network': {},
    'skalenetwork': {},
}

colors = [
    '#808080',
    '#000000',
    '#800000',
    '#808000',
    '#008000',
    '#008080',
    '#000080',
    '#800080',
    '#049900',
    '#0099A5',
    '#420083',
    '#83004A',
    '#44845B',
    '#945A5A',
    '#8D0055',
]

FREVSINFRE = {
    '2017-Q1': {},
    '2017-Q2': {},
    '2017-Q3': {},
    '2017-Q4': {},
    '2018-Q1': {},
    '2018-Q2': {},
    '2018-Q3': {},
    '2018-Q4': {},
    '2019-Q1': {},
    '2019-Q2': {},
    '2019-Q3': {},
    '2019-Q4': {},
    '2020-Q1': {},
    '2020-Q2': {},
    '2020-Q3': {},
    '2020-Q4': {},
}


def contributors():
    df = pd.read_csv('contributors.csv')
    orgs = df.groupby(by='organization').sum()['contribudores']
    print(np.array(orgs))
    ct = Counter(df['organization'])
    print(sum(ct.values()))


def total_devs():
    df = pd.read_csv('data/commits.csv', encoding='utf-8')
    # Necesito contar los desarrolladores de manera unica por mes
    print(df.sort_values(by='date').iloc[0])
    ts_date = pd.to_datetime(df['date']).sort_values()

    dates = np.datetime_as_string(ts_date.values)
    print(dates[0], dates[-1])
    contador = {}
    for ind, date in enumerate(dates):
        if int(dates[ind][5: 7]) <= 3:
            dates[ind] = dates[ind][0: 4] + '-Q1'
        elif int(dates[ind][5: 7]) <= 6:
            dates[ind] = dates[ind][0: 4] + '-Q2'
        elif int(dates[ind][5: 7]) <= 9:
            dates[ind] = dates[ind][0: 4] + '-Q3'
        elif int(dates[ind][5: 7]) <= 12:
            dates[ind] = dates[ind][0: 4] + '-Q4'
        contador[dates[ind]] = 0

    names = pd.Series(data=df.sort_values(by='date')['name'])
    print(names)
    print(dates)
    print(contador)

    """
        Necesito comparar dentro de un semestre todos los de la lista de ese semestre
        Agarro el total y lo itero hasta que sea otro mes y cuento la cantidad de devs unicos
    """
    ct_fechas = Counter(dates)
    del ct_fechas['2021-Q1']
    del contador['2021-Q1']

    proyectos_list = []
    pos_ant = 0
    print(ct_fechas)
    for key in sorted(ct_fechas.keys()):
        print(f"{pos_ant}:{(pos_ant + ct_fechas[key])}")
        proyectos_list.append(names.iloc[pos_ant:(pos_ant + ct_fechas[key])])
        pos_ant += (ct_fechas[key] + 1)

    set_dict = []
    for i, v in enumerate(proyectos_list):
        set_dict.append(len(set(v)))
        contador[sorted(ct_fechas.keys())[i]] = len(set(v))

    x = [str(x) for x in contador]
    y = set_dict
    plt.style.use('seaborn')
    plt.plot(x, y, scalex=True)
    plt.xlabel('Year')
    plt.ylabel('Devs Count')
    plt.title('Developers count trough quarters of a year')
    plt.xticks(rotation=60)
    plt.tight_layout()
    plt.grid(True)
    plt.legend()
    plt.show()


def avg_contrib_per_month():
    df = pd.read_csv('data/commits.csv', encoding='utf-8')
    df = df.sort_values(by='date')[['name', 'date']]
    lista = []
    for i in df.values:
        if i[1][0:4] != '2021' and i[1][0:4] != '2013' and i[1][0:4] != '2014' and i[1][0:4] != '2015' and i[1][0:4] != '2016':
            lista.append(f'{i[1].replace("T", "-")}-{i[0]}')

    dict_anios = {}
    for i in sorted(lista):
        dict_anios[i.split('-')[0] + i.split('-')[1]] = {}

    print(dict_anios)
    for k in dict_anios:
        for j in range(1, 32):
            dict_anios[k][str(j)] = {'names': []}
            for elem in sorted(lista):
                if int(elem.split('-')[2]) == j and elem.split('-')[0] + elem.split('-')[1] == k:
                    if elem.split('-')[4] in dict_anios[k][str(j)]['names']:
                        continue
                    else:
                        dict_anios[k][str(j)]['names'].append(elem.split('-')[4])

    cantidad_devs = []
    conteo_total = []
    for i in dict_anios:
        cont = 0
        _nombres = []
        for j in dict_anios[i]:
            if len(dict_anios[i][j]['names']) > 0:
                cont += 1
                _nombres.append(dict_anios[i][j]['names'])

        cantidad_devs.append(_nombres)
        conteo_total.append(cont)

    print(cantidad_devs)
    conteo_devs = {}
    for ind, (dev, cont) in enumerate(zip(cantidad_devs, conteo_total)):
        conteo_devs[ind] = {}
        for i in dev:
            if len(i) > 1:
                for j in i:
                    if j in conteo_devs[ind]:
                        conteo_devs[ind][j] += 1
                    else:
                        conteo_devs[ind][j] = 1
            else:
                if i[0] in conteo_devs[ind]:
                    conteo_devs[ind][i[0]] += 1
                else:
                    conteo_devs[ind][i[0]] = 1

    sumador = []
    for k in conteo_devs:
        sumador.append(sum(conteo_devs[k].values()) / len(conteo_devs[k].items()))

    x = [str(x)[0:4] + '-' + str(x)[4:6] for x in dict_anios]
    y = sumador
    plt.style.use('seaborn')
    mean = [np.array(y).mean() for _ in y]
    median = [np.median(y) for _ in y]
    plt.plot(x, y, color='#4ac', scalex=True, linewidth=1)
    plt.fill_between(x, y, color='#4ac', alpha=0.5)
    plt.plot(x, mean, color='#048', label='Mean', linestyle='dashed', linewidth=2)
    plt.plot(x, median, color='#848', label='Median', linestyle='dashed', linewidth=2)
    plt.xlabel('Months')
    plt.ylabel('Days contributed by devs')
    plt.title('Days contributed in avg by devs per month')
    plt.xticks(rotation=75)
    plt.tight_layout()
    plt.grid(True)
    plt.legend()
    plt.show()


def frequent_vs_infrequent():
    df = pd.read_csv('commits.csv', encoding='utf-8')
    df = df.sort_values(by='date')[['name', 'date']]
    lista = []
    for i in df.values:
        if i[1][0:4] != '2021':
            lista.append(f'{i[1].replace("T", "-")}-{i[0]}')

    dict_anios = {}
    for i in sorted(lista):
        dict_anios[i.split('-')[0] + i.split('-')[1]] = {}

    print(dict_anios)
    for k in dict_anios:
        for j in range(1, 32):
            dict_anios[k][str(j)] = {'names': []}
            for elem in sorted(lista):
                if int(elem.split('-')[2]) == j and elem.split('-')[0] + elem.split('-')[1] == k:
                    if elem.split('-')[4] in dict_anios[k][str(j)]['names']:
                        continue
                    else:
                        dict_anios[k][str(j)]['names'].append(elem.split('-')[4])

    cantidad_devs = []
    conteo_total = []
    for i in dict_anios:
        cont = 0
        _nombres = []
        for j in dict_anios[i]:
            if len(dict_anios[i][j]['names']) > 0:
                cont += 1
                _nombres.append(dict_anios[i][j]['names'])

        cantidad_devs.append(_nombres)
        conteo_total.append(cont)

    print(cantidad_devs)
    conteo_devs = {}
    for ind, (dev, cont) in enumerate(zip(cantidad_devs, conteo_total)):
        conteo_devs[ind] = {}
        for i in dev:
            if len(i) > 1:
                for j in i:
                    if j in conteo_devs[ind]:
                        conteo_devs[ind][j] += 1
                    else:
                        conteo_devs[ind][j] = 1
            else:
                if i[0] in conteo_devs[ind]:
                    conteo_devs[ind][i[0]] += 1
                else:
                    conteo_devs[ind][i[0]] = 1

    contador_frequent = []
    contador_infrequent = []
    cont = 0
    for k in conteo_devs:
        contador_frequent.append(0)
        contador_infrequent.append(0)
        for i in conteo_devs[k]:
            if conteo_devs[k][i] > 10:
                contador_frequent[cont] += 1
            else:
                contador_infrequent[cont] += 1

        cont += 1

    print(contador_frequent)
    print(len(contador_frequent))
    print(contador_infrequent)
    print(len(contador_infrequent))

    x = [str(x)[0:4] + '-' + str(x)[4:6] for x in dict_anios]
    y1 = contador_frequent
    y2 = contador_infrequent
    plt.style.use('seaborn')
    plt.plot(x, y1, scalex=True, label='Frequent devs', color='#2ECC71')
    plt.plot(x, y2, scalex=True, label='Infrequent devs', color='#FEC233')
    plt.xlabel('Months')
    plt.ylabel('Devs count')
    plt.title('Frequent vs Infrequent devs')
    plt.xticks(rotation=75)
    plt.tight_layout()
    plt.grid(True)
    plt.legend()
    plt.show()


def sizes_of_teams():
    df = pd.read_csv('commits.csv', encoding='utf-8')
    y = []
    for i in df.groupby(by='org')['name'].unique().values:
        y.append(len(i))

    x = df.groupby(by='org')['name'].count().index
    print(y)
    print(x)

    y = np.array(y)
    plt.style.use('ggplot')
    plt.scatter(x, y, color='#2ECC71', linewidth=1.5, label="devs", s=200)
    y1 = [y.mean() for _ in y]
    plt.plot(y1, color='#009094', linewidth=2, label='mean', linestyle='dashed')
    # plt.scatter(l_x[num], l_y[num], color='#2ECC71')
    plt.ylabel('Projects')
    plt.xlabel('Team size')
    plt.title('Team size for project')
    # plt.fill_between(x, y, alpha=0.25, color='#2ECC71')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.legend()
    plt.grid(True)
    plt.show()


def bonus():
    df = pd.read_csv('commits.csv', encoding='utf-8')
    cont_mas = 0
    cont_menos = 0
    for i in list(df.groupby(by='name')['org'].unique()):
        if len(i) > 1:
            cont_mas += 1
        else:
            cont_menos += 1

    plt.style.use('ggplot')
    plt.barh(['Mono Project', 'Multi Project'], [cont_menos, cont_mas], color='#009094', linewidth=2, label="devs")
    # plt.plot(y1, color='#009094', linewidth=2, label='mean', linestyle='dashed')
    # plt.scatter(l_x[num], l_y[num], color='#2ECC71')
    plt.ylabel('Projects')
    plt.xlabel('Devs count')
    plt.title('Developers that develop in one vs in more than one project')
    # plt.fill_between(x, y, alpha=0.25, color='#2ECC71')
    ticks = [x for x in range(0, 700, 40)]
    plt.xticks(ticks, rotation=0)
    plt.tight_layout()
    plt.legend()
    plt.grid(True)
    plt.show()


def grow_first_commit():
    df = pd.read_csv('data/commits.csv')
    df.sort_values(by='date', inplace=True)
    for i in list(df[['date', 'org']].values):
        if i[0][0:4] != '2021' and i[0][0:4] != '2013' and i[0][0:4] != '2014' and i[0][0:4] != '2015' and i[0][0:4] != '2016':
            for k in ORGANIZATIONS:
                if i[0][0:4] + 'Q1' in ORGANIZATIONS[k]:
                    pass
                else:
                    ORGANIZATIONS[k][i[0][0:4] + 'Q1'] = 0
                if i[0][0:4] + 'Q2' in ORGANIZATIONS[k]:
                    pass
                else:
                    ORGANIZATIONS[k][i[0][0:4] + 'Q2'] = 0
                if i[0][0:4] + 'Q3' in ORGANIZATIONS[k]:
                    pass
                else:
                    ORGANIZATIONS[k][i[0][0:4] + 'Q3'] = 0
                if i[0][0:4] + 'Q4' in ORGANIZATIONS[k]:
                    pass
                else:
                    ORGANIZATIONS[k][i[0][0:4] + 'Q4'] = 0

            if int(i[0][5:7]) <= 3:
                ORGANIZATIONS[i[1]][i[0][0:4] + 'Q1'] += 1
            elif int(i[0][5:7]) <= 6:
                ORGANIZATIONS[i[1]][i[0][0:4] + 'Q2'] += 1
            elif int(i[0][5:7]) <= 9:
                ORGANIZATIONS[i[1]][i[0][0:4] + 'Q3'] += 1
            elif int(i[0][5:7]) <= 12:
                ORGANIZATIONS[i[1]][i[0][0:4] + 'Q4'] += 1

    print(df[(df['org'] == 'omgnetwork') & (df['date'].str.contains('2016'))])

    for k in ORGANIZATIONS:
        print(k)
        print()
        print(ORGANIZATIONS[k])
        print('-----')

    plt.rcParams.update({'figure.autolayout': True})
    plt.style.use('ggplot')
    cont = 0
    print(len(list(ORGANIZATIONS['omgnetwork'].keys())))
    x = np.arange(len(list(ORGANIZATIONS['omgnetwork'].keys())))
    total_list = np.zeros(len(x))
    for k in ORGANIZATIONS:
        # plt.plot(
        #     list(ORGANIZATIONS['omgnetwork'].keys()),
        #     list(ORGANIZATIONS[k].values()),
        #     label=k,
        #     color=colors[cont],
        #     alpha=0.88,
        #     linewidth=0.8
        # )
        total_list += np.array(list(ORGANIZATIONS[k].values()))
        cont += 1

    x = list(ORGANIZATIONS['omgnetwork'].keys())
    mean_list = [np.array(total_list).mean() for _ in total_list]
    median_list = [np.median(total_list) for _ in total_list]
    plt.plot(x, total_list, label='Total', color='#EC7063', linewidth=2.5, alpha=0.95)
    plt.fill_between(x, total_list, color='#EC7063', alpha=0.4)
    # plt.plot(x, mean_list, label='Mean', color='#220863', linestyle='dashed', linewidth=1.5, alpha=0.75)
    # plt.plot(x, median_list, label='Median', color='#FF08F3', linestyle='dashed', linewidth=1.5, alpha=0.75)
    plt.ylabel('Commits')
    plt.xlabel('Time')
    plt.title('Commits trough project')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.)
    # plt.grid(True)
    plt.show()


def gained_devs():
    df = pd.read_csv('data/commits.csv')
    df.sort_values(by='date', inplace=True)
    df = df[~(df['date'].str.contains('2021'))]  # Asi saco todos los del 2021
    df['date'] = pd.to_datetime(df['date'])
    for i, j, k, l in zip(df['date'].dt.month, df['date'].dt.year, df['name'], df['org']):
        print(j, i, k, l)
        if j == 2013 or j == 2014 or j == 2015 or j == 2016:
            continue

        for key in ORGANIZATIONS:
            if i <= 3:
                if str(j) + '-Q1' in ORGANIZATIONS[key]:
                    pass
                else:
                    ORGANIZATIONS[key][str(j) + '-Q1'] = {'cantidad': 0, 'nombres': []}
            elif i <= 6:
                if str(j) + '-Q2' in ORGANIZATIONS[key]:
                    pass
                else:
                    ORGANIZATIONS[key][str(j) + '-Q2'] = {'cantidad': 0, 'nombres': []}
            elif i <= 9:
                if str(j) + '-Q3' in ORGANIZATIONS[key]:
                    pass
                else:
                    ORGANIZATIONS[key][str(j) + '-Q3'] = {'cantidad': 0, 'nombres': []}
            elif i <= 12:
                if str(j) + '-Q4' in ORGANIZATIONS[key]:
                    pass
                else:
                    ORGANIZATIONS[key][str(j) + '-Q4'] = {'cantidad': 0, 'nombres': []}

        if i <= 3:
            if str(j) + '-Q1' in ORGANIZATIONS[l]:
                if k in ORGANIZATIONS[l][str(j) + '-Q1']['nombres']:
                    pass
                else:
                    ORGANIZATIONS[l][str(j) + '-Q1']['cantidad'] += 1
                    ORGANIZATIONS[l][str(j) + '-Q1']['nombres'].append(k)
        elif i <= 6:
            if str(j) + '-Q2' in ORGANIZATIONS[l]:
                if k in ORGANIZATIONS[l][str(j) + '-Q2']['nombres']:
                    pass
                else:
                    ORGANIZATIONS[l][str(j) + '-Q2']['cantidad'] += 1
                    ORGANIZATIONS[l][str(j) + '-Q2']['nombres'].append(k)
        elif i <= 9:
            if str(j) + '-Q3' in ORGANIZATIONS[l]:
                if k in ORGANIZATIONS[l][str(j) + '-Q3']['nombres']:
                    pass
                else:
                    ORGANIZATIONS[l][str(j) + '-Q3']['cantidad'] += 1
                    ORGANIZATIONS[l][str(j) + '-Q3']['nombres'].append(k)
        elif i <= 12:
            if str(j) + '-Q4' in ORGANIZATIONS[l]:
                if k in ORGANIZATIONS[l][str(j) + '-Q4']['nombres']:
                    pass
                else:
                    ORGANIZATIONS[l][str(j) + '-Q4']['cantidad'] += 1
                    ORGANIZATIONS[l][str(j) + '-Q4']['nombres'].append(k)

    print(ORGANIZATIONS)
    valores_x = {}
    valores_y = list(ORGANIZATIONS['omgnetwork'])
    for k in ORGANIZATIONS:
        valores_x[k] = {}
        for j in ORGANIZATIONS[k]:
            valores_x[k][j] = ORGANIZATIONS[k][j]['cantidad']

    plt.rcParams.update({'figure.autolayout': True})
    plt.style.use('ggplot')
    cont = 0
    start = 0
    finish = 15
    cont_color = -1
    total_list = np.zeros(len(valores_y))
    for k in valores_x:
        if finish > cont >= start:
            total_list += list(valores_x[k].values())
            # plt.plot(
            #     list(valores_x[k].keys()),
            #     list(valores_x[k].values()),
            #     label=k,
            #     color=colors[cont_color],
            #     alpha=0.9,
            #     linewidth=1.2
            # )
        cont += 1
        cont_color += 1

    # print(total_list)
    # print(sorted(total_list))
    # avg_list_devs = total_list / 15
    median_line = [np.median(total_list) for _ in total_list]
    # plt.plot(valores_y, median_line, label='Median', color='#220863', linestyle='dashed', linewidth=2.5, alpha=0.75)
    plt.plot(valores_y, total_list, label='Devs across projects', color='#220863', linewidth=1.5, alpha=0.95)
    plt.fill_between(valores_y, total_list, color='#220863', alpha=0.4)
    plt.ylabel('Devs')
    plt.xlabel('Time')
    plt.title('Devs trough projects')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)
    # plt.grid(True)
    plt.show()


def rank_devs():
    df = pd.read_csv('commits.csv')
    df.sort_values(by='date', inplace=True)
    df = df[~(df['date'].str.contains('2021'))]  # Asi saco todos los del 2021
    df['date'] = pd.to_datetime(df['date'])
    ranking = df.groupby('org')['name'].value_counts()
    mapping = {}
    for i in ranking.index:
        if i[0] in mapping:
            mapping[i[0]] += 1
        else:
            mapping[i[0]] = 1

    print(sorted(mapping.items(), key=lambda z: z[1]))
    y = [y[1] for y in sorted(mapping.items(), key=lambda z: z[1])]
    print(df[df['org'] == 'starkware-libs'])
    x = [x[0] for x in sorted(mapping.items(), key=lambda z: z[1])]
    plt.style.use('ggplot')
    plt.barh(x, y, color='#EC7063')
    plt.ylabel('Projects')
    plt.xlabel('Devs')
    plt.title('Rank of dev quantity for every project')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.legend()
    plt.grid(True)
    plt.show()


def rank_commits():
    df = pd.read_csv('commits.csv')
    df.sort_values(by='date', inplace=True)
    df = df[~(df['date'].str.contains('2021'))]  # Asi saco todos los del 2021
    df['date'] = pd.to_datetime(df['date'])
    ranking = df.groupby('org').count().sort_values(by='project', ascending=False)['name']
    print(ranking)
    print(sum(list(ranking.values)))
    y = list(ranking.values)
    x = list(ranking.index)
    plt.style.use('ggplot')
    plt.barh(x, y, color=colors[6])
    plt.ylabel('Projects')
    plt.xlabel('Commits')
    plt.title('Rank of commits for every project')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.legend()
    plt.grid(True)
    plt.show()


def devs_commit_each_month():
    df = pd.read_csv('commits.csv')
    df.sort_values(by='date', inplace=True)
    df = df[~(df['date'].str.contains('2021'))]  # Asi saco todos los del 2021
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    for k in ORGANIZATIONS:
        for i in range(1, 13):
            ORGANIZATIONS[k][i] = {'cantidad': 0, 'nombres': []}

    for k in ORGANIZATIONS:
        filt = (df['org'] == k)
        for val, ind in zip(list(df[filt][['org', 'name']].resample('M').agg(['unique']).values), list(df[filt][['org', 'name']].resample('M').agg(['unique']).index)):
            print(ind.month)
            if len(val[0]) > 0:
                for nombre in val[1]:
                    if nombre in ORGANIZATIONS[k][ind.month]['nombres']:
                        pass
                    else:
                        ORGANIZATIONS[k][ind.month]['cantidad'] += 1
                        ORGANIZATIONS[k][ind.month]['nombres'].append(nombre)

    print(ORGANIZATIONS)
    y = {}
    for k in ORGANIZATIONS:
        y[k] = {}
        for j in ORGANIZATIONS[k]:
            y[k][j] = ORGANIZATIONS[k][j]['cantidad']

    plt.style.use('ggplot')
    width = 0.15
    print(y)
    start = 0
    finish = 15
    cont1 = 0
    cont2 = -2
    x = np.array([x for x in range(1, 13)])
    for k in y:
        if start <= cont1 < finish:
            plt.bar(x + (width*cont2), list(y[k].values()),
                    color=colors[cont1], width=width,
                        label=k, alpha=1)
            cont2 += 1

        cont1 += 1

    plt.ylabel('Quantity of active devs')
    plt.xlabel('Months')
    plt.title('Quantity of devs for every month')
    plt.xticks(x, rotation=0)
    plt.tight_layout()
    plt.legend(loc="upper left", title="Projects")
    plt.grid(True)
    plt.show()


def fre_vs_infre():
    df = pd.read_csv('data/commits.csv')
    df.sort_values(by='date', inplace=True)
    df = df[~(df['date'].str.contains('2021'))]  # Asi saco todos los del 2021
    df['date'] = pd.to_datetime(df['date'])
    for i in list(df.values):
        print(i[3], i[4].year, i[4].month, i[4].day)
        _nombre = str(i[3])
        _anio = str(i[4].year)
        _mes = str(i[4].month)
        _dia = str(i[4].day)
        if _anio == '2013' or _anio == '2014' or _anio == '2015' or _anio == '2016':
            continue

        if int(_mes) <= 3:
            if _nombre in FREVSINFRE[_anio+'-Q1']:
                if _mes+_dia in FREVSINFRE[_anio + '-Q1'][_nombre]:
                    pass
                else:
                    FREVSINFRE[_anio + '-Q1'][i[3]].append(_mes+_dia)
            else:
                FREVSINFRE[_anio + '-Q1'][_nombre] = []
                FREVSINFRE[_anio + '-Q1'][_nombre].append(_mes+_dia)
        elif int(_mes) <= 6:
            if _nombre in FREVSINFRE[_anio + '-Q2']:
                if _mes + _dia in FREVSINFRE[_anio + '-Q2'][_nombre]:
                    pass
                else:
                    FREVSINFRE[_anio + '-Q2'][i[3]].append(_mes + _dia)
            else:
                FREVSINFRE[_anio + '-Q2'][_nombre] = []
                FREVSINFRE[_anio + '-Q2'][_nombre].append(_mes + _dia)
        elif int(_mes) <= 9:
            if _nombre in FREVSINFRE[_anio + '-Q3']:
                if _mes + _dia in FREVSINFRE[_anio + '-Q3'][_nombre]:
                    pass
                else:
                    FREVSINFRE[_anio + '-Q3'][i[3]].append(_mes + _dia)
            else:
                FREVSINFRE[_anio + '-Q3'][_nombre] = []
                FREVSINFRE[_anio + '-Q3'][_nombre].append(_mes + _dia)
        elif int(_mes) <= 12:
            if _nombre in FREVSINFRE[_anio + '-Q4']:
                if _mes + _dia in FREVSINFRE[_anio + '-Q4'][_nombre]:
                    pass
                else:
                    FREVSINFRE[_anio + '-Q4'][i[3]].append(_mes + _dia)
            else:
                FREVSINFRE[_anio + '-Q4'][_nombre] = []
                FREVSINFRE[_anio + '-Q4'][_nombre].append(_mes + _dia)
        print('---')

    x = list(FREVSINFRE.keys())
    y_fre = []
    y_infre = []
    for k in FREVSINFRE:
        print(k)
        print(FREVSINFRE[k])
        print()
        if len(FREVSINFRE[k]) > 0:
            cont_fre = 0
            for j in FREVSINFRE[k]:
                if len(FREVSINFRE[k][j]) > 10:
                    cont_fre += 1

            y_fre.append(cont_fre)
            y_infre.append(len(FREVSINFRE[k]) - cont_fre)
        else:
            y_fre.append(0)
            y_infre.append(0)

    plt.rcParams.update({'figure.autolayout': True})
    plt.style.use('ggplot')
    mean_fre = [np.array(y_fre).mean() for _ in x]
    mean_infre = [np.array(y_infre).mean() for _ in x]
    width = 2
    plt.plot(x, y_infre, label='Infrequent devs', color='#196F3D', linewidth=width)
    plt.fill_between(x, y_infre, color='#196F3D', alpha=0.5)
    plt.plot(x, y_fre, label='Frequent devs', color='#EC7063', linewidth=width)
    plt.fill_between(x, y_fre, color='#EC7063', alpha=0.5)
    plt.plot(x, mean_fre, label='Frequent devs mean', color='#EC7063', linestyle='dashed')
    plt.plot(x, mean_infre, label='Infrequent devs mean', color='#196F3D', linestyle='dashed')
    plt.xlabel('Quarters')
    plt.ylabel('Devs count')
    plt.title('Frequent vs Infrequent devs')
    plt.xticks(x, rotation=75)
    plt.tight_layout()
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.show()


gained_devs()
