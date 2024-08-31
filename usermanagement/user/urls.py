from django.urls import path
from .views import create_user, custom_404_view, login_user, is_logged_in, logout_user, list_users

handler404 = custom_404_view

urlpatterns = [
    path('login_user/', login_user, name='login_user'),
    path('create_user/', create_user, name='create_user'),
    path('is_logged_in/', is_logged_in, name='is_logged_in'),
    path('logout_user/', logout_user, name='logout_user'),
    path('list_users/', list_users, name='list_users')

]

