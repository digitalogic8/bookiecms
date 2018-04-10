from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

from django.template import loader
from django.contrib.auth import logout

def index(request):
     if request.user.is_authenticated:
         return HttpResponse("Hello, you. You're at the bookie index.")
     else:
        return loginPage(request) 
def loginPage(request):
    template = loader.get_template('registration/login.html')
    context = {}
    return HttpResponse(template.render(context,request))
def loginUser(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        userGroups = []
        for group in user.groups.all():
            userGroups.append(group.name)
        if "bookie" in userGroups:
            return redirect('/bookie', request)
        else:
            return redirect('/better', request)
    else:
        return HttpResponse("You are NOT logged in.")
def logout_view(request):
    logout(request)
    return loginPage(request) 
    # Redirect to a success page.