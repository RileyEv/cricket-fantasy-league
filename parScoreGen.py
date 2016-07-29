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
API_KEY = '1ee0d0a07cbc2669663a434020f184da'
SEASONS = ['2013', '2014', '2015', '2016']
TEAM_ID = '98565'
POSITIONS = {
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
            if match_data['innings'][0]['team_batting_id'] == TEAM_ID:
                innings = match_data['innings'][0]
            else:
                innings = match_data['innings'][1]
            POSITIONS[i][0].append(innings['runs'])
            for bat in innings['bat']:
                if bat['how_out'] == 'did not bat':
                    POSITIONS[i][int(bat['position'])].append('dnb')
                    print(bat['position'], 'dnb')
                else:
                    if bat['runs'] == '':
                        bat['runs'] = 0
                    POSITIONS[i][int(bat['position'])].append(int(bat['runs']))
                    print(bat['position'], bat['runs'])
    print(POSITIONS)

for k, v in POSITIONS.iteritems():
    f = open('{}.csv'.format(k), 'w')
    writer = csv.writer(f)
    for i in v:
        writer.writerow(i)
    f.close()
