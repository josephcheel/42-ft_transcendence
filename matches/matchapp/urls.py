from django.urls import path
from .views import propose_match, get_pending_matches

urlpatterns = [
    path('propose_match/', propose_match, name='propose_match'),
    path('get_pending_matches/', get_pending_matches, name='get_pending_matches'),
]

