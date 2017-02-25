# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
import json
from .player import Player


class Match():
    def __init__(self, match_id, players):
        self.match_id = match_id
        self.api_key = ""
        self.team_id = "98565"
        self.players = players
        self.get_match_details()
        self.which_team()
        self.create_players()

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
            self.players[
                str(i['player_id'])
            ] = Player(
                self.match_id,
                i['player_id'],
                i['player_name'],
            )
