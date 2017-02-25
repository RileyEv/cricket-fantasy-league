# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
import json
import csv
from datetime import datetime


def get_data(url):
    r = requests.get(url)
    if r.ok:
        return json.loads(r.content)
    else:
        r.raise_for_status()

API_URL = 'http://www.play-cricket.com/api/v2/'
API_KEY = ''
SEASONS = ['2011', '2012', '2013', '2014', '2015', '2016']
TEAM_ID = '64265'
POSITIONS = {
    '2011': [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    ],
    '2012': [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    ],
    '2013': [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    ],
    '2014': [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    ],
    '2015': [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    ],
    '2016': [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    ],
}

for i in SEASONS:
    matches = get_data(
        '{0}matches.json?site_id=3808&api_token={1}&season={2}&team_id={3}'.format(
            API_URL,
            API_KEY,
            i,
            TEAM_ID,
        )
    )['matches']
    for match in matches:
        if match['status'] != 'Deleted' and datetime.strptime(match['match_date'], '%d/%m/%Y') < datetime.now():
            match_data = get_data(
                '{0}match_detail.json?match_id={1}&api_token={2}'.format(
                    API_URL,
                    match['id'],
                    API_KEY,
                )
            )['match_details'][0]
            if match_data['result'] != 'A' and match_data['result'] != '':
                if match_data['innings'][0]['team_batting_id'] == TEAM_ID:
                    innings = match_data['innings'][0]
                else:
                    innings = match_data['innings'][1]
                for n in range(11):
                    try:
                        bat = innings['bat'][n]
                    except IndexError:
                        bat = {'how_out': 'did not bat', 'position': str(n + 1)}
                    if bat['how_out'] == 'did not bat':
                        POSITIONS[i][int(bat['position']) - 1].append('dnb')
                        print(bat['position'], 'dnb')
                    else:
                        if bat['runs'] == '':
                            bat['runs'] = 0
                        POSITIONS[i][int(bat['position']) - 1].append(int(bat['runs']))
                        print(bat['position'], bat['runs'])
            else:
                print('abandoned')
    print(POSITIONS)

ALL_SEASONS = [
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
]

for k, v in POSITIONS.iteritems():
    # f = open('{}.csv'.format(k), 'w')
    # writer = csv.writer(f)
    n = 0
    for i in v:
        # writer.writerow(i)
        ALL_SEASONS[n] += i
        n += 1
    # f.close()


AVERAGES = []
total_score = 0.0
f = open('all.csv', 'w')
writer = csv.writer(f)
for i in ALL_SEASONS:
    writer.writerow(i)
    position_total = 0
    for score in i:
        if score != 'dnb':
            position_total += int(score)
    mean = position_total / float(len(i))
    AVERAGES.append(
        {
            'mean': mean,
        }
    )
    total_score += mean
f.close()

for i in range(len(AVERAGES)):
    AVERAGES[i]['percentage'] = 100 * (AVERAGES[i]['mean'] / total_score)

print()
print()
print(AVERAGES)
