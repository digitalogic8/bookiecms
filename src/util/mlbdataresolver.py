'''
Created on May 3, 2018

@author: digitalogic8
'''
from __future__ import print_function
import mlbgame
from datetime import datetime, timedelta
if __name__ == '__main__':

    #'away_team', 'away_team_errors', 'away_team_hits', 'away_team_runs',
    # 'date', 'game_id', 'game_league', 'game_start_time', 'game_status', 
    #'game_tag', 'home_team', 'home_team_errors', 'home_team_hits', 'home_team_runs', 
    #'l_pitcher', 'l_pitcher_losses', 'l_pitcher_wins', 'l_team', 'nice_score', 
    #'sv_pitcher', 'sv_pitcher_saves', 'w_pitcher', 'w_pitcher_losses', 'w_pitcher_wins', 
    #'w_team']
    yesterday = datetime.datetime.now()- timedelta(days=1)
    month = mlbgame.games(yesterday.year, yesterday.month, yesterday.day)
    games = mlbgame.combine_games(month)
    teams = mlbgame.info.team_info()
    teamMap = {}
    for team in teams:
        teamMap[team["club_common_name"]] = team["display_code"].upper()
    for game in games:
        print(teamMap[game.w_team])