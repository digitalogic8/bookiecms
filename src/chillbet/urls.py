"""chillbet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
#from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('better/', include('better.urls')),
    path('bookie/', include('bookie.urls')),
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.loginPage, name='login'),
    path('loginuser/', views.loginUser, name='loginUser'),
    #url(r'^login/$', auth_views.login, {'template_name': 'core/login.html'}, name='login'),
    #path('logout/', auth_views.logout, name='logout'),
    path('admin/', admin.site.urls),
]
