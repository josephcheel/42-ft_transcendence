from django.test import TestCase, Client
from django.urls import reverse
from .views import create_user
import json

class UserModelTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = {"username" : "test1", "password" : "test"}
        self.user2 = {"username" : "test2", "password" : "test"}
        self.base_json = {
            'status': None,
            'message': None,
            'data': None
        }