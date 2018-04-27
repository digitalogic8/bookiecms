import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

from django.core.wsgi import get_wsgi_application
import os


def scrapeOdds(sport):
    # Collect and parse first page
    page = requests.get('https://www.covers.com/Sports/'+sport+'/Odds/Matchups/US/SPREAD/competition/Online/ML')
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # Pull all text from the BodyText div
    artist_name_list = soup.find(class_='covers-CoversOdds-Table responsive')
    
    # Pull text from all instances of <a> tag within BodyText div
    artist_name_list_items = artist_name_list.find_all('tr')
    returnData = []
    for tableRow in artist_name_list_items:
        gameData = {}
        tds = tableRow.find_all('td')
        if len(tds) == 0: 
            continue
        gameDetails = tds[0]
        
        dateTime = gameDetails.find(class_='cover-CoversOdds-tableTime').string.strip()
        dateTime = ' '.join(dateTime.split())
        teams         = gameDetails.find_all(class_="cover-CoversOdds-details-Team")
        team1= teams[0].find(class_="cover-CoversOdds-tableTeamLink").a.string.strip()
        team2= teams[1].find(class_="cover-CoversOdds-tableTeamLink").a.string.strip()
        oddsRow = []
        for oddsBrick in tds[1:]:
            oddBricki = oddsBrick.find_all('span')
            if len(oddBricki) == 4:
                home = {"spread" : oddBricki[0].string, "moneyline" : oddBricki[1].string}
                away = {"spread" : oddBricki[2].string, "moneyline" : oddBricki[3].string}
                osetter = {"home":home, "away":away}
                oddsRow.append(osetter)
        gameData["home"] = team1
        gameData["away"] = team2
        gameData["time"] = dateTime
        gameData["odds"] = oddsRow
        returnData.append(gameData)
    blah = {"games" : returnData}
    print(json.dumps(blah, indent=4, sort_keys=True))
    return blah

from better.models import Team, Contest
sport = "MLB"
data = scrapeOdds(sport)
for gameData in data["games"]:
    try:
        awayTeam = Team.objects.filter(teamAbbreviation=gameData["away"])[0]
    except:
        print (gameData["away"] + " is not in the db")
        continue
    try:
        homeTeam = Team.objects.filter(teamAbbreviation=gameData["home"])[0]
    except:
        print (gameData["home"] + " is not in the db")
        continue
    if awayTeam and homeTeam:
        #Apr 20, 7:05 PM ET
        #YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]
        timeArray = gameData["time"].split(' ')
        month = timeArray[0]
        day = timeArray[1].rstrip(',').zfill(2)
        hour = timeArray[2].split(":")[0].zfill(2)
        minute = timeArray[2].split(":")[1].zfill(2)
        ampm = timeArray[3]
        tz = timeArray[4]
        gametime = datetime.strptime(month + day + hour + minute + ampm + "2018",'%b%d%I%M%p%Y')
        contest = Contest(homeTeam = homeTeam, awayTeam = awayTeam, contest_date=gametime)
        #line=gameData["odds"][0]["away"]["moneyline"]
        contest.save()


        
   # contest.save()
    
    
#         homeTeam = models.ForeignKey(Team, related_name='homeTeam', on_delete=models.CASCADE)
#     awayTeam = models.ForeignKey(Team, related_name='awayTeam', on_delete=models.CASCADE)
#     overUnder = models.FloatField()
#     line = models.FloatField()
#     contestPhoto = models.URLField()
#     contest_date = models.DateTimeField('Date Of Contest')
    
    
    print(gameData["away"])
