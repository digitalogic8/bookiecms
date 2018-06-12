from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from better.models import Contest, AvailableBets
from better.models import Bet
from django.shortcuts import redirect
from datetime import date, timedelta, datetime


def index(request):
    if request.method == 'POST':
        amount = request.POST.get('betAmount', '')
        displayedOdds = request.POST.get('displayedOdds', '')
        bet = request.POST.get('bet', '')
        betType = AvailableBets.objects.get(pk=bet)
        #if the displayed odds don't match what we currently have we need to notify the user

        timestamp = datetime.now()
        numberOfBet =  betType
        line = float(betType.odds)
        amountOfBet = float(amount)
        approved = False
        outcome = 'N' 
        bet = Bet(timestamp=timestamp, numberOfBet=numberOfBet, userMakingBet=request.user.username, line=line, amountOfBet=amountOfBet, approved=approved, outcome=outcome)
        bet.save()
    userGroups = []
    if not request.user.is_authenticated:
        return redirect('/', request)
    user = request.user
    for group in user.groups.all():
        userGroups.append(group.name)
    if "bookie" in userGroups:
        return redirect('/bookie', request)
    contests = Contest.objects.filter(contest_date__gte=date.today()- timedelta(1))
    template = loader.get_template('better/chillbet.html')
    displayData = []
    for contest2 in contests:
        displayData.append({"availableBets" : AvailableBets.objects.filter(contest=contest2), "contest": contest2})
    context = {
        'contests': displayData,
    }
    return HttpResponse(template.render(context, request))
def betHistory(request):
    userGroups = []
    if not request.user.is_authenticated:
        return redirect('/', request)
    user = request.user
    for group in user.groups.all():
        userGroups.append(group.name)
    if "bookie" in userGroups:
        return redirect('/bookie', request)
    bets = Bet.objects.filter(userMakingBet=request.user.username)
    template = loader.get_template('better/betHistory.html')
    
    context = {
        'bets': bets,
    }
    return HttpResponse(template.render(context, request)) 
