# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from stats.match import Match

m = Match('2761566', {})

n = Match('2761568', m.players)

print(n.players)

