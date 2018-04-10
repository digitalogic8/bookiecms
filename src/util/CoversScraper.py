import requests

from bs4 import BeautifulSoup

import json





proxies = {

  'http': 'http://www-proxy.us.oracle.com:80',

  'https': 'http://www-proxy.us.oracle.com:80'

}



# Collect and parse first page

page = requests.get('https://www.covers.com/Sports/NCAAB/Odds/Matchups/US/SPREAD/competition/Online/ML', proxies=proxies)

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



print(json.dumps(blah))

