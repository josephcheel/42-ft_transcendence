from django.test import TestCase, Client
from django.urls import reverse
from .views import propose_match, get_pending_matches
from .models import Invitation
import json
from django.contrib.auth import  get_user_model
from datetime import datetime, timedelta
from django.utils import timezone


User = get_user_model()

class CreateInvitationTests(TestCase):

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
        current_time = datetime.now()
        time_delta = timedelta(minutes=5)
        future_time = current_time + time_delta
        self.future_time_str = future_time.isoformat()

    def check_json(self, response, code):
        self.assertJSONEqual(json.dumps(self.base_json), response.content.decode("utf-8"))
        self.assertEqual(response.status_code, code)        

    def test_propose_match(self):

        self.base_json['status'] = 'success'
        self.base_json['message'] = 'Sent invitations to all players'
        jsonTest = {
            'start_time': self.future_time_str,
            'players': [self.user1['username'], self.user2['username']]
        }      
        response = self.client.post(reverse(propose_match), jsonTest, content_type='application/json')
        self.check_json(response, 200)

    def test_propose_match_no_start_time(self):
        self.base_json['status'] = 'error'
        self.base_json['message'] = 'Invalid Json body'
        jsonTest = {
            'start_time': self.future_time_str,
        }       
        response = self.client.post(reverse(propose_match), jsonTest, content_type='application/json')
        self.check_json(response, 400)

    def test_propose_match_no_players(self):
        self.base_json['status'] = 'error'
        self.base_json['message'] = 'Invalid Json body'
        jsonTest = {
            'players': [self.user1['username'], self.user2['username']]
        }    
        response = self.client.post(reverse(propose_match), jsonTest, content_type='application/json')
        self.check_json(response, 400)

    def test_no_valid_user_propose_match(self):
        self.base_json['status'] = 'error'
        self.base_json['message'] = 'A user does not exist'
        jsonTest = {
            'start_time': self.future_time_str,
            'players': [self.user1['username'], "I am not a user"]
        }       
        response = self.client.post(reverse(propose_match), jsonTest, content_type='application/json')
        self.check_json(response, 404)

    def test_not_enough_players_user_propose_match(self):
        self.base_json['status'] = 'error'
        self.base_json['message'] = 'Needs more than one player'
        
        ## Test with just 1 players
        jsonTest = {
            'start_time': self.future_time_str,
            'players': [self.user1['username']]
        }     
        response = self.client.post(reverse(propose_match), jsonTest, content_type='application/json')
        self.check_json(response, 400)
        





class CreatedInvitationsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.base_json = {
            'status': None,
            'message': None,
            'data': None
        }
        current_time = timezone.now()
        
        # Add a timedelta to the current time
        time_delta = timedelta(minutes=5)
        self.future_time = current_time + time_delta
        
        # Convert to ISO format
        self.future_time_str = self.future_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'


        self.user1 = {"username" : "test1", "password" : "test1"}
        self.user2 = {"username" : "test2", "password" : "test2"}
        User.objects.create_user(username=self.user1['username'], password=self.user1['password'])
        User.objects.create_user(username=self.user2['username'], password=self.user2['password'])
        Invitation.objects.create(
            creation_time=current_time,
            start_time=self.future_time,
            player_id= User.objects.get(username=self.user1['username']),
            owner = True,
            status = 1,
            )
        Invitation.objects.create(
            creation_time=current_time,
            start_time=self.future_time,
            player_id= User.objects.get(username=self.user2['username']),
            )
        
    def check_json(self, response, code):

        self.assertJSONEqual(json.dumps(self.base_json), response.content.decode("utf-8"))
        self.assertEqual(response.status_code, code)        
    
    
    def test_check_pending_matches(self):

        self.base_json['status'] = 'success'
        self.base_json['message'] = 'retrived all pending invitations'
        self.base_json['data'] = []

        # Test Player Has No pending 
        jsonTest = {'player': self.user1['username']}
        response = self.client.get(reverse('get_pending_matches'), data=jsonTest)
        self.check_json(response, 200)


        # Test Player Has One Pending
        jsonTest = {'player': self.user2['username']}
        response = self.client.get(reverse(get_pending_matches), data=jsonTest)

        response_data = json.loads(response.content.decode("utf-8"))
        if response_data:
            creation_time = response_data['data'][0]['creation_time']

        self.base_json['data'] = [{
            'creation_time': creation_time,
            'owner': False,
            'player_id': 2,
            'start_time': self.future_time_str,
            'status': '2'

        }]
        self.check_json(response, 200)

        # Test player doesn't exist
        jsonTest = {'player': 'No existo'}
        response = self.client.get(reverse('get_pending_matches'), data=jsonTest)
        self.base_json['data'] = None
        self.base_json['status'] = 'error'
        self.base_json['message'] = 'A user does not exist'


        self.check_json(response, 404)

        

