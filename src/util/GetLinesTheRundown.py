import csv
import os
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os
from dateutil import parser

#

import urllib.request, json 

def getSportsIdForSport(sportName):
    with urllib.request.urlopen("https://therundown.io/api/v1/sports") as url:
        returnData = json.loads(url.read().decode())
        for sport in returnData.get("sports"):
            if sportName in sport.get("sport_name"):
                return sport.get("sport_id")
    return 0

def getUpcomingGames(sport):
    from better.models import AvailableBets, Team, Contest
    # Collect and parse first page
    sportsId = getSportsIdForSport(sport)
    with urllib.request.urlopen("https://therundown.io/api/v1/sports/" + str(sportsId) + "/events") as url:
        returnData = json.loads(url.read().decode())
        for event in returnData.get("events"):
            for team in event.get("teams"):
                if team["is_away"]:
                    for normalTeam in event.get("teams_normalized"):
                        if normalTeam.get("team_id") == team.get("team_id"):
                            awayTeam = Team.objects.filter(teamAbbreviation=normalTeam.get("abbreviation"))[0]
                else:
                    for normalTeam in event.get("teams_normalized"):
                        if normalTeam.get("team_id") == team.get("team_id"):
                            homeTeam = Team.objects.filter(teamAbbreviation=normalTeam.get("abbreviation"))[0]
             
            if awayTeam and homeTeam:
                gametime = parser.parse(event["event_date"])
                if len(Contest.objects.filter(homeTeam = homeTeam, awayTeam = awayTeam, contest_date=gametime)) == 0:
                    contest = Contest(homeTeam = homeTeam, awayTeam = awayTeam, contest_date=gametime)
                
                    contest.save()
                else:
                    print (" game exists")
                contest = Contest.objects.get(homeTeam = homeTeam, awayTeam = awayTeam, contest_date=gametime)
                
                line = event["lines"]["1"] #the one on this case is the odds maker, eventually we will want to allows the user to set the odds maker

            #moneyline
                AvailableBets.objects.filter(contest=contest, bettype="moneyline").delete()
                availBet = AvailableBets(contest=contest, bettype="moneyline", odds=line["moneyline"]["moneyline_home"], team=homeTeam)
                availBet.save()
                availBet2 = AvailableBets(contest=contest, bettype="moneyline", odds=line["moneyline"]["moneyline_away"], team=awayTeam)
                availBet2.save()
            #spread
                AvailableBets.objects.filter(contest=contest, bettype="spread").delete()
                availBet = AvailableBets(contest=contest, bettype="spread", odds=line["spread"]["point_spread_home_money"],spread=line["spread"]["point_spread_home"], team=homeTeam)
                availBet.save()
                availBet2 = AvailableBets(contest=contest, bettype="spread", odds=line["spread"]["point_spread_away_money"],spread=line["spread"]["point_spread_away"], team=awayTeam)
                availBet2.save()
            #total
                AvailableBets.objects.filter(contest=contest, bettype="total").delete()
                availBet = AvailableBets(contest=contest, bettype="total", odds=line["total"]["total_over_money"], spread=line["total"]["total_over"], overorunder="over", team=homeTeam)
                availBet.save()
                availBet2 = AvailableBets(contest=contest, bettype="total", odds=line["total"]["total_under_money"], spread=line["total"]["total_under"], overorunder="under", team=awayTeam)
                availBet2.save()



    
def buildTeams():
    
    from better.models import Team
    with open('/code/util/allBaseballTeams.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            if len(Team.objects.filter(teamAbbreviation=row[0])) == 0:
                team = Team(teamAbbreviation=row[0], teamName=row[2], sport="MLB", teamLogo=row[4])
                team.save()

if __name__ == "__main__":
    print (getUpcomingGames("MLB"))
