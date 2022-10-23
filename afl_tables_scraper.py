import requests
from bs4 import BeautifulSoup
import csv
import numpy as np

current_year = 2004
earliest_year = 2003

# player_stats scraper
for year in range(current_year - earliest_year + 1):
    source = requests.get('https://afltables.com/afl/stats/' + str(current_year - year) + 'a.html').text

    soup = BeautifulSoup(source, 'lxml')
    tbody = soup.find('tbody')
    if (current_year - year) == 2017:
        print(soup.prettify())
    table = []

    for datas in tbody.find_all('td'):

        data = datas.text
        table.append(data)

    arr = np.array(table)
    two_dimensional_table = np.reshape(arr, (-1, 25))

    with open('player_stats_' + str(current_year - year) + ".csv", "w+", newline='', encoding='utf-8') as stats_csv:
        csv_writer = csv.writer(stats_csv, delimiter=',')
        csv_writer.writerow(
            ['Player', 'Team', 'Games', 'Kicks', 'Marks', 'Handballs',
             'Disposals', 'Goals', 'Behinds', 'Hit Outs', 'Tackles',
             'Rebound 50s', 'Inside 50s', 'Clearances', 'Clangers', 'Frees For',
             'Frees Against', 'Brownlow Votes', 'Contested Possessions',
             'Uncontested Possessions', 'Contested Marks', 'Marks Inside 50',
             'One Percenters', 'Bounces', 'Goal Assists'])
        csv_writer.writerows(two_dimensional_table)

# team_stats_for_ scraper
for year in range(current_year - earliest_year + 1):
    source = requests.get('https://afltables.com/afl/stats/' + str(current_year - year) + 's.html').text

    soup = BeautifulSoup(source, 'lxml')
    tbody = soup.find_all('tbody')
    table = []

    for data in tbody[0].find_all('td'):
        table.append(data.text)

    arr = np.array(table)
    two_dimensional_table = np.reshape(arr, (-1, 22))

    with open("team_stats_for_" + str(current_year - year) + ".csv", "w+", newline='', encoding='utf-8') as stats_csv:
        csv_writer = csv.writer(stats_csv, delimiter=',')
        csv_writer.writerow(
            ['Team', 'Kicks', 'Marks', 'Handballs',
             'Disposals', 'Goals', 'Behinds', 'Hit Outs', 'Tackles',
             'Rebound 50s', 'Inside 50s', 'Clearances', 'Clangers', 'Frees For',
             'Brownlow Votes', 'Contested Possessions',
             'Uncontested Possessions', 'Contested Marks', 'Marks Inside 50',
             'One Percenters', 'Bounces', 'Goal Assists'])
        csv_writer.writerows(two_dimensional_table)


# team_stats_against_ scraper
for year in range(current_year - earliest_year + 1):
    source = requests.get('https://afltables.com/afl/stats/' + str(current_year - year) + 's.html').text

    soup = BeautifulSoup(source, 'lxml')
    tbody = soup.find_all('tbody')
    table = []

    for data in tbody[1].find_all('td'):
        table.append(data.text)

    arr = np.array(table)
    two_dimensional_table = np.reshape(arr, (-1, 22))

    with open("team_stats_against_" + str(current_year - year) + ".csv", "w+", newline='', encoding='utf-8') as stats_csv:
        csv_writer = csv.writer(stats_csv, delimiter=',')
        csv_writer.writerow(
            ['Team', 'Kicks', 'Marks', 'Handballs',
             'Disposals', 'Goals', 'Behinds', 'Hit Outs', 'Tackles',
             'Rebound 50s', 'Inside 50s', 'Clearances', 'Clangers', 'Frees For',
             'Brownlow Votes', 'Contested Possessions',
             'Uncontested Possessions', 'Contested Marks', 'Marks Inside 50',
             'One Percenters', 'Bounces', 'Goal Assists'])
        csv_writer.writerows(two_dimensional_table)

# games played scraper
games_source = requests.get('https://afltables.com/afl/stats/biglists/bg2.txt').text

games_source_raw_li = games_source.split("\n")
del games_source_raw_li[0:3]
games_li = []

# clean up data
for raw_row in games_source_raw_li:
    row = raw_row.split()
#     # remove . from the index and clean up
    if len(row) > 0:
        r = row[0].split('.')
        del row[0]
        if len(r) > 1:
            row.insert(0, r[0])
            if r[1] != '':
                row.insert(1, r[1])

    # join De Koning style last names, remove and replace old entries
    if len(row) > 6:

        last_name = " ".join(row[4:6])
        del row[4:6]
        row.insert(4, last_name)
        games_li.append(row)

    elif len(row) == 0:
        pass

    else:
        games_li.append(row)

# remove all asterisks from current players
for row in games_li:
    if len(row) > 0:
        row[1] = row[1].replace('*', '')

for i in games_li[0:10]:
    print(i)

with open("games_played.csv", "w+", newline='', encoding='utf-8') as games_played_csv:
    csv_writer = csv.writer(games_played_csv)
    csv_writer.writerow(
        ['Player Number', 'Games Played', 'W-D-L',
         'First Name', 'Last Name', 'For'])
    csv_writer.writerows(games_li)

import requests
from bs4 import BeautifulSoup
import csv
import numpy as np

# there are a three players missing birthdays but they are from the 19th century so it won't matter much to me
DOB_debut_source = requests.get('https://afltables.com/afl/stats/biglists/bg10.txt').text

DOB_debut_raw_li = DOB_debut_source.split("\n")
del DOB_debut_raw_li[0:1]

DOB_debut_li = []

for raw_row in DOB_debut_raw_li:
    row = raw_row.split()
    if len(row) > 0:
        r = row[0].split('.')
        del row[0]
        if len(r) > 1:
            row.insert(0, r[0])
            if r[1] != '':
                row.insert(1, r[1])

    if len(row) > 9:
        last_name = " ".join(row[2:4])
        del row[2:4]
        row.insert(2, last_name)
        del row[6:7]
        DOB_debut_li.append(row)
    elif len(row) == 0:
        pass
    else:
        del row[6:7]
        DOB_debut_li.append(row)

for row in DOB_debut_li:
    row[6] = row[6].replace('SM', 'SY')
    row[5] = row[5].replace('SM', 'SY')
    row[5] = row[5].replace('KA', 'NM')

for row in DOB_debut_li:
    if len(row) == 8:
        row[7] = row[7].replace('*', '')
        if len(row[3]) == 10:
            row[3] = '0' + row[3]
        if len(row[7]) == 10:
            row[7] = '0' + row[7]
        player_id = row[1][:1] + row[2][:1] + row[5] + row[3].replace('-', '') + row[7].replace('-', '')
        row.insert(0, player_id)

with open("DOB_debut.csv", "w+", newline='', encoding='utf-8') as DOB_debut_csv:
    csv_writer = csv.writer(DOB_debut_csv)
    csv_writer.writerow(
        ['Player ID', 'Player Number', 'First Name', 'Last Name',
         'DOB', 'Round', 'For', 'Against', 'Debut Date'])
    csv_writer.writerows(DOB_debut_li)