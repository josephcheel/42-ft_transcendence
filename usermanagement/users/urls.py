from django.urls import path
from .views import create_user, login

urlpatterns = [
    path('create_user/', create_user, name='create_user'),
    path('list_users/', create_user, name='list_users'),
    path('login/', login, name='list_users'),
]

