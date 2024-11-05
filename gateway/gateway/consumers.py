import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import requests
import logging
from .signals import *

logger = logging.getLogger('django')
logger.setLevel(logging.DEBUG)


class UserConsumer(WebsocketConsumer):
    def connect(self):
        #self.notify_user_management('online')
        logger.debug("I am about to accept a connection")
        #async_to_sync(user_connected.send)(sender=self.__class__)
        self.accept()

    def disconnect(self, close_code):
        logger.debug("I am about to disconnect")

        self.notify_user_management('offline')
        user_disconnected.send(sender=self.__class__)

    
    def notify_user_management(self, status):
        data = {
            'username': self.user.username,
            'status': status
        }
        # Send an HTTP POST request to the user management service
        async_to_sync(self.send_request)(data)

    async def send_request(self, data):
        response = await requests.post(f'http://usermanagement:8000/user/status')
        print(response.body)