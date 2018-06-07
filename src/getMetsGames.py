#!python
from __future__ import print_function
import mlbgame

month = mlbgame.games(2018, 5, 1)
games = mlbgame.combine_games(month)
for game in games:
    print(game)
