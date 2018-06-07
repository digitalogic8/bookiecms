import csv
import os
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os
from better.models import AvailableBets


def scrapeOdds(sport):
    # Collect and parse first page
    returnData = []
    for type in ["MONEYLINE", "SPREAD", "TOTAL"]:
        page = requests.get('https://www.covers.com/Sports/'+sport+'/Odds/Matchups/US/'+type+'/competition/Online/ML')
        soup = BeautifulSoup(page.text, 'html.parser')
        
        # Pull all text from the BodyText div
        theTable = soup.find(class_='covers-CoversOdds-Table responsive')
        
        # Pull text from all instances of <a> tag within BodyText div
        theGames = theTable.find_all('tr')

        for tableRow in theGames:
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
                    if type=='MONEYLINE':
                        row1 = {"odds" : oddBricki[0].string}
                        row2 = {"odds" : oddBricki[2].string}
                        osetter = {team1:row1, team2:row2, "type": type}
                        oddsRow.append(osetter)
                    if type=='TOTAL':
                        row1 = {"over" : oddBricki[0].string, "odds" : oddBricki[1].string}
                        row2 = {"under" : oddBricki[2].string, "odds" : oddBricki[3].string}
                        osetter = {"over":row1, "under":row2, "type": type}
                        oddsRow.append(osetter)
                    if type=='SPREAD':
                        row1 = {"spread" : oddBricki[0].string, "odds" : oddBricki[1].string}
                        row2 = {"spread" : oddBricki[2].string, "odds" : oddBricki[3].string}
                        osetter = {team1:row1, team2:row2, "type": type}
                        oddsRow.append(osetter)
                break #if you want odds from all sources don't do this but i jus twant 5 dimes
            gameData["home"] = team1
            gameData["away"] = team2
            gameData["time"] = dateTime
            gameData["odds"] = oddsRow
            matchFound = False
            for game in returnData:
                if game["home"] == team1 and game["away"] == team2:
                    matchFound = True
                    for odd in gameData["odds"]:
                        game["odds"].append(odd)
            if not matchFound:       
                returnData.append(gameData)
    blah = {"games" : returnData}
    print(json.dumps(blah, indent=4, sort_keys=True))
    return blah

def buildGames(sport="MLB"):
    from better.models import Team, Contest
    from better.models import Team
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
            if len(Contest.objects.filter(homeTeam = homeTeam, awayTeam = awayTeam, contest_date=gametime)) == 0:
                contest = Contest(homeTeam = homeTeam, awayTeam = awayTeam, contest_date=gametime)
                #line=gameData["odds"][0]["away"]["moneyline"]
                contest.save()
            else:
                print (" game exists")
            contest = Contest.objects.get(homeTeam = homeTeam, awayTeam = awayTeam, contest_date=gametime)
            
            for betType in gameData["odds"]:
                bettype = betType["type"]
                
                if bettype == "MONEYLINE":
                    AvailableBets.objects.filter(contest=contest, bettype="moneyline").delete()
                    availBet = AvailableBets(contest=contest, bettype="moneyline", odds=betType[homeTeam.teamAbbreviation]["odds"], team=homeTeam)
                    availBet.save()
                    availBet2 = AvailableBets(contest=contest, bettype="moneyline", odds=betType[awayTeam.teamAbbreviation]["odds"], team=awayTeam)
                    availBet2.save()
                if bettype == "SPREAD":
                    AvailableBets.objects.filter(contest=contest, bettype="spread").delete()
                    availBet = AvailableBets(contest=contest, bettype="spread", odds=betType[homeTeam.teamAbbreviation]["odds"],spread=betType[homeTeam.teamAbbreviation]["spread"], team=homeTeam)
                    availBet.save()
                    availBet2 = AvailableBets(contest=contest, bettype="spread", odds=betType[awayTeam.teamAbbreviation]["odds"],spread=betType[awayTeam.teamAbbreviation]["spread"], team=awayTeam)
                    availBet2.save()
                if bettype == "TOTAL":
                    AvailableBets.objects.filter(contest=contest, bettype="total").delete()
                    availBet = AvailableBets(contest=contest, bettype="total", odds=betType["over"]["odds"], spread=betType["over"]["over"][:-1], overorunder="over", team=homeTeam)
                    availBet.save()
                    availBet2 = AvailableBets(contest=contest, bettype="total", odds=betType["under"]["odds"], spread=betType["under"]["under"][:-1], overorunder="under", team=awayTeam)
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
    scrapeOdds("MLB")