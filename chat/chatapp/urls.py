from django.urls import path
from .views import send_message, test_check

urlpatterns = [
    path('send_message/', send_message, name='send_message'),
    path('test_check/', test_check, name='test_check')
]

