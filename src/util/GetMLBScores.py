import urllib.request, json 
from datetime import date, timedelta
from better.models import Contest

def updateScores():
    yesterday = date.today() - timedelta(1)
    year = str(yesterday.year)
    day = str(yesterday.day)
    if len(day) < 2:
        day = "0" + day
    month = str(yesterday.month)
    if len(month) < 2:
        month = "0" + month
    with urllib.request.urlopen("http://gd2.mlb.com/components/game/mlb/year_"+year+"/month_"+month+"/day_"+day+"/master_scoreboard.json") as url:
        data = json.loads(url.read().decode())
        gameData = []
        for game in data["data"]["games"]["game"]:
            gamer = {}
            gamer["homeTeam"] = game.get("home_name_abbrev")
            gamer["awayTeam"] = game.get("away_name_abbrev") 
            gamer["awayScore"] = game.get("linescore").get("r").get("away")
            gamer["homeScore"] = game.get("linescore").get("r").get("home")
            gamer["time"] = game.get("time")
            gameData.append(gamer)
        #does not account for double headers probably need to compare times
        try:
            for contest in Contest.objects.filter(contest_date__date=yesterday):
                print (contest)
                for game in gameData:
                    if contest.homeTeam.teamAbbreviation == game["homeTeam"]:
                        contest.homeScore = game["homeScore"]
                        contest.awayScore = game["awayScore"]
                        contest.save()
        except:
            pass
                    
updateScores()
        
        
        


