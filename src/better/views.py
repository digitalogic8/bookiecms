from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from better.models import Contest, AvailableBets
from better.models import Bet
from django.shortcuts import redirect

def index(request):
    userGroups = []
    if not request.user.is_authenticated:
        return redirect('/', request)
    user = request.user
    for group in user.groups.all():
        userGroups.append(group.name)
    if "bookie" in userGroups:
        return redirect('/bookie', request)
    contests = Contest.objects.all()
    template = loader.get_template('better/chillbet.html')
    displayData = []
    for contest2 in contests:
        displayData.append({"availableBets" : AvailableBets.objects.filter(contest=contest2), "contest": contest2})
    context = {
        'contests': displayData,
    }
    return HttpResponse(template.render(context, request))
def takeABet(request, betNumber, amount):
    pass
