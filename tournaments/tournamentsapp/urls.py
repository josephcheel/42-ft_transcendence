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
from tournamentsapp.views.open_tournament import open_tournament
from tournamentsapp.views.accept_invitation import accept_invitation
from tournamentsapp.views.close_tournament import close_tournament
from tournamentsapp.tasks.finish_tournament import finish_tournament
from tournamentsapp.views.start_match import start_match
from tournamentsapp.views.finish_match import finish_match
from tournamentsapp.views.list_tournaments import list_tournaments, list_tournaments_status
from tournamentsapp.views.list_matches import list_matches, list_matches_by_tournament_id, list_not_played_matches
from tournamentsapp.views.list_invitations import list_invitations
from tournamentsapp.views.edit_tournament import edit_tournament
from tournamentsapp.views.get_next_match import get_next_match
from tournamentsapp.views.disconnect_user import disconnect_user


urlpatterns = [
    path('open_tournament/',open_tournament),
    path('edit_tournament/',edit_tournament),
    path('accept_invitation/',accept_invitation),
    path('close/',close_tournament),
    path('finish/',finish_tournament),
    path('start_match/',start_match),
    path('finish_match/', finish_match),
    path('list_tournaments/<str:username>/',
         list_tournaments, name='list_tournaments'),
    path('list_tournaments_status/<str:username>/',
         list_tournaments_status, name='list_tournaments_status'),
    path('list_matches/<str:username>/', list_matches, name='list_matches'),
    path('list_not_played_matches/<str:username>/',
         list_not_played_matches, name='list_not_played_matches'),
    path('list_matches_by_tournament_id/<str:tournament_id>/',
         list_matches_by_tournament_id, name='list_matches_by_tournament_id'),
    path('list_invitations/<str:username>/', list_invitations, name = 'list_invitations'),
    path('get_next_match/<str:username>/', get_next_match, name = 'get_next_match'),
    path('disconnect_user', disconnect_user, name = 'disconnect_user'),

]
