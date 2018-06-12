from django.urls import path

from better import views

urlpatterns = [
    path('', views.index, name='index'),
    path('betHistory/', views.betHistory, name='betHistory')
]