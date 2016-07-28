# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
import json
from numpy import mean
from numpy import std
from numpy import array


class Match():
    def __init__(self, match_id, players):
        self.match_id = match_id
        self.api_key = "1ee0d0a07cbc2669663a434020f184da"
        self.team_id = "98565"
        self.players = players
        self.get_match_details()
        self.which_team()
        self.create_players()
        self.calculate_bat_innings()

    def __str__(self):
        return self.match_id

    def get_match_details(self):
        url = "http://www.play-cricket.com/api/v2/match_detail.json?match_id={0}&api_token={1}"
        r = requests.get(
            url.format(
                self.match_id,
                self.api_key,
            )
        )
        if r.ok:
            self.match_data = json.loads(r.content)['match_details'][0]
        else:
            r.raise_for_status()

    def which_team(self):
        if self.match_data['home_team_id'] == self.team_id:
            self.team = 'home_team'
        else:
            self.team = 'away_team'

    def create_players(self):
        if self.team == 'home_team':
            index = 0
        else:
            index = 1
        for i in self.match_data['players'][index][self.team]:
            if str(i['player_id']) not in list(self.players.keys()):
                self.players[str(i['player_id'])] = {
                    'name': i['player_name'],
                    str(self.match_id): {
                        'bat': None,
                        'bowl': None,
                        'field': None,
                        'bonus': None,
                    },
                }
            else:
                self.players[str(i['player_id'])][str(self.match_id)] = {
                    'bat': None,
                    'bowl': None,
                    'field': None,
                    'bonus': None,
                }

    def strike_rate_enabled(self, innings):
        enabled = True
        for i in innings['bat']:
            if i['how_out'] not in ['did not bat', 'ro', 'no']:
                if i['balls'] == '':
                    i['balls'] = 0
                    enabled = False
                    break
        return enabled

    def calculate_par_scores(self, innings):
        runs = innings['runs']
        return {
            '1': 0.14 * runs,
            '2': 0.13 * runs,
            '3': 0.13 * runs,
            '4': 0.12 * runs,
            '5': 0.11 * runs,
            '6': 0.09 * runs,
            '7': 0.07 * runs,
            '8': 0.06 * runs,
            '9': 0.04 * runs,
            '10': 0.03 * runs,
            '11': 0.02 * runs,
            'extras': 0.06 * runs,
        }

    def calculate_mean_std(self, arr):  # Pass in array of numbers to be calculated on
        arr = array(arr)
        return mean(arr), std(arr)

    def calculate_bat_innings(self):
        # only battings figures added
        if self.match_data['innings'][0]['team_batting_id'] == self.team_id:
            innings = self.match_data['innings'][0]
        else:
            innings = self.match_data['innings'][1]
        if self.strike_rate_enabled(innings):
            strike_rates = []
            for i in innings['bat']:
                if i['balls'] != 0:
                    strike_rates.append((float(i['runs']) / float(i['balls'])) * 100.0)
            mean, std = self.calculate_mean_std(strike_rates)
            print(strike_rates)
            print(mean, std)

    def bowl_innings(self):
        # blowing + fielding figures added
        if self.match_data['innings'][0]['team_battingid'] == self.team_id:
            innings = self.match_data['innings'][1]
        else:
            innings = self.match_data['innings'][0]
        print(innings)
