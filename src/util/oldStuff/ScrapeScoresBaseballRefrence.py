'''
Created on Jun 19, 2018
@author: digitalogic8
'''
import requests
from bs4 import BeautifulSoup
import datetime
from datetime import date, timedelta
from util.mlbdataresolver import yesterday
from better.models import AvailableBets, Team, Contest



def getScores(month, day, year):
    # Collect and parse first page
    page = requests.get('https://www.baseball-reference.com/boxes/?month='+month+'&day='+day+'&year=' + year)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # Pull all text from the BodyText div
    boxScores = soup.find_all(class_='teams')
    scores = []
    for boxScore in boxScores:
    # Pull text from all instances of <a> tag within BodyText div
        teams = boxScore.find_all('tr')
        game = []
        for tableRow in teams:
            tds = tableRow.find_all('td')
            team = {}
            team["name"] = tds[0].find('a').string
            team["score"] = tds[1].string
            game.append(team)
        scores.append(game)
    return scores
#     
yesterday = date.today() - timedelta(1)
data = scrapeOdds(str(yesterday.month), str(yesterday.day), str(yesterday.year))
for contest in Contest.objects.filter(contest_date=yesterday):
    print (contest.homeTeam)
print(data)
