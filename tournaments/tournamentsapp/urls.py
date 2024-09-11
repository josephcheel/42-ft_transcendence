"""
URL configuration for tournaments project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from tournamentsapp.views.views import open_tournament, accept_invitation, close_tournament, finish_tournament, start_match, finish_match
from tournamentsapp.views.list_tournaments import list_tournaments


urlpatterns = [
    path('list/',list_tournaments),
    path('open/',open_tournament),
    path('accept_invitation/',accept_invitation),
    path('close/',close_tournament),
    path('finish/',finish_tournament),
    path('start_match/',start_match),
    path('finish_match/', finish_match),
    path('list_tournaments/', list_tournaments),

]
