from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from better.models import Contest
from better.models import Bet

def index(request):
    contests = Contest.objects.all()
    template = loader.get_template('better/chillbet.html')
    context = {
        'contests': contests,
    }
    return HttpResponse(template.render(context, request))
def takeABet(request, betNumber, amount):
    pass
