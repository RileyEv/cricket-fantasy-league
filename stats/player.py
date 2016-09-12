# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class Player():
    def __init__(self, match_id, user_id, player_name):
        self.match_id = match_id
        self.user_id = user_id
        self.player_name = player_name
        self.match_data = {
            'bat': {
                'runs': 0,
                'par_score': 0,
            },
            'bowl': {
                'wickets': {
                    'lbw': 0,
                    'bowled': 0,
                    'stumped': 0,
                    'caught': 0,
                    'hit_wicket': 0,
                },
                'overs': 0,
                'runs': 0,
                'maidens': 0,
            },
            'fielding': {
                'catches': 0,
                'run_outs': 0,
                'stumpings': 0,
            },
        }
