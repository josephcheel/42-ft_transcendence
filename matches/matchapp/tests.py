from django.test import TestCase, Client
from django.urls import reverse
from .views import propose_match
import json
from django.contrib.auth import  get_user_model
from datetime import datetime, timedelta

User = get_user_model()

class usermodelTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.base_json = {
            'status': None,
            'message': None,
            'data': None
        }
        self.user1 = {"username" : "test1", "password" : "test1"}
        self.user2 = {"username" : "test2", "password" : "test2"}
        User.objects.create_user(username=self.user1['username'], password=self.user1['password'])
        User.objects.create_user(username=self.user2['username'], password=self.user2['password'])

        


    def check_json(self, response, code):
        self.assertJSONEqual(json.dumps(self.base_json), response.content.decode("utf-8"))
        self.assertEqual(response.status_code, code)        
    ## Necesito saber el formato a usar para la hora
    def test_propose_match(self):
        current_time = datetime.now()
        time_delta = timedelta(minutes=5)
        # Calculate the time 5 minutes from now
        future_time = current_time + time_delta
        future_time_str = future_time.isoformat()
        jsonTest = json.dumps({
            'start_time': future_time_str,
            'players': [self.user1['username'], self.user2['username']]
        })        
        response = self.client.post(reverse(propose_match), jsonTest, content_type='application/json')
        print(response.content.decode("utf-8"))

        pass