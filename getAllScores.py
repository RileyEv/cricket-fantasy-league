# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
import json
import csv
from datetime import datetime

import plotly.plotly as py
import plotly.graph_objs as go

import numpy

def get_data(url):
    r = requests.get(url)
    if r.ok:
        return json.loads(r.content)
    else:
        r.raise_for_status()

def remove_outliers(arr):
    elements = numpy.array(arr)

    mean = numpy.mean(elements, axis=0)
    sd = numpy.std(elements, axis=0)

    final_list = [x for x in arr if (x > mean - 2 * sd)]
    final_list = [x for x in final_list if (x < mean + 2 * sd)]

    return final_list

API_URL = 'http://www.play-cricket.com/api/v2/'
API_KEY = ''
SEASONS = ['2011', '2012', '2013', '2014', '2015', '2016', '2017']
TEAM_IDS = ['64264', '64264', '98565']
POSITIONS = {
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    6: [],
    7: [],
    8: [],
    9: [],
    10: [],
    11: [],
}
# for season in SEASONS:
#     for i in range(11):
#         POSITIONS[i][season] = []

total_matches = 0
for team in TEAM_IDS:
    for i in SEASONS:
        matches = get_data(
            '{0}matches.json?site_id=3808&api_token={1}&season={2}&team_id={3}'.format(
                API_URL,
                API_KEY,
                i,
                team,
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
                if match_data['result'] != 'A' and match_data['result'] != '' and len(match_data['innings']) not in [0,1]:
                    total_matches += 1
                    if match_data['innings'][0]['team_batting_id'] == team:
                        innings = match_data['innings'][0]
                    else:
                        innings = match_data['innings'][1]
                    total_runs = 0
                    for bat in innings['bat']:
                        total_runs += int(bat['runs'] if bat['runs'] != '' else 0)
                    if total_runs != 0:
                        for n in range(11):
                            try:
                                bat = innings['bat'][n]
                            except IndexError:
                                bat = {'how_out': 'did not bat', 'position': str(n + 1)}
                            if bat['how_out'] != 'did not bat':
                                if bat['runs'] == '':
                                    bat['runs'] = 0
                                POSITIONS[int(bat['position'])].append((int(bat['runs'])/total_runs)*100)
print('Saving')

f = open('allScores.csv', 'w', newline='')
writer = csv.writer(f)
for i in range(11):
    POSITIONS[i+1] = remove_outliers(POSITIONS[i+1])
    for item in POSITIONS[i+1]:
        writer.writerow([i+1,item])
f.close()

print()
print('Done')
