from django.urls import path

from better import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('betHistory/', views.betHistory, name='betHistory')
]