from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from bookie.forms import SignUpForm
from bookie.models import BookieProfile
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.models import Group



def index(request):
    template = loader.get_template('bookie/chillbetadmin.html')
    context = {
        'bets': "",
    }
    return HttpResponse(template.render(context, request))

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            #save profile data
            user.refresh_from_db()  # load the profile instance created by the signal
            betterProfile = BookieProfile(user=user, siteName=form.cleaned_data.get('siteName'), email=form.cleaned_data.get('email'))
            betterProfile.save()
            group = Group.objects.get(name='bookie')
            user.groups.add(group)
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/bookie')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})