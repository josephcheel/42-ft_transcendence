from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/gateway/', consumers.UserConsumer.as_asgi()),
]