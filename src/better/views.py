from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from better.models import Contest, AvailableBets
from better.models import Bet
from django.shortcuts import redirect
from datetime import date, timedelta, datetime
from better.forms import SignUpForm
from django.contrib.auth import authenticate, login
from better.models import BetterProfile
from better.models import Team



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
    template = loader.get_template('better/chillbet.html')
    sports = ["NFL", "MLB", "NCAAF"]
    contests = {}
    for sport in sports:
        contestsSport = Contest.objects.filter(contest_date__gte=date.today()- timedelta(1), homeTeam__sport=sport)
        displayData = []
        for contest2 in contestsSport:
            displayData.append({"availableBets" : AvailableBets.objects.filter(contest=contest2), "contest": contest2})
        contests[sport] = displayData
    


    context = {
        'contests': contests,
        'sports' : sports
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

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            #save profile data
            user.refresh_from_db()  # load the profile instance created by the signal
            bookie = BookieProfile.get(siteName=form.cleaned_data.get('siteName'))
            betterProfile = BetterProfile(user=user, bookie=bookie, email=form.cleaned_data.get('email'))
            betterProfile.save()
            
            
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/better')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
