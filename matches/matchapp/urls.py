from django.urls import path
from .views import propose_match

urlpatterns = [
    path('propose_match/', propose_match, name='propose_match'),
]

