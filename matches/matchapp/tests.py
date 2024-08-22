from django.test import TestCase, Client
from django.urls import reverse
from .views import propose_match
import json

class usermodelTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = {"username" : "test1", "password" : "test"}
        self.user2 = {"username" : "test2", "password" : "test"}
        self.base_json = {
            'status': None,
            'message': None,
            'data': None
        }
    def test_propose_match(self):
        