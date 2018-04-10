from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from better.models import Contest
from bookie.models import Bets


def index(request):
    bets = Bets.objects.all()
    template = loader.get_template('bookie/chillbetadmin.html')
    context = {
        'bets': bets,
    }
    return HttpResponse(template.render(context, request))