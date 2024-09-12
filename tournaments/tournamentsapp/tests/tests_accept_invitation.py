from tournamentsapp.models import Tournaments, Invitations, Matches, User
from django.test import TestCase, Client
from django.urls import reverse
from tournamentsapp.views import open_tournament, accept_invitation, close_tournament, start_match, finish_match
from tournamentsapp.views.list_tournaments import list_tournaments
from datetime import timedelta
from django.utils import timezone
from django.db import OperationalError
import json
from tournamentsapp.status_options import StatusTournaments, StatusInvitations, StatusMatches, Rounds
import random
from .printing import print_all_tournaments, print_all_invitations, print_all_matches, print_all_users
from datetime import datetime
# Create your tests here.
#User = get_user_model()

class test_accept_invitation (TestCase):
	def setUp(self):
		self.client = Client()
		self.users = []
		for i in range(1, 22):
			current_user = User.objects.create(username=f"test{i}", password="test")

	def check_json(self, response, code):
		self.assertJSONEqual(json.dumps(self.base_json),
		                     response.content.decode("utf-8"))
		self.assertEqual(response.status_code, code)

	def test_accept_invitation(self):
		self.base_json = {'status': None, 'message': None, 'data': None}
		self.tournament = {
			'username': 'test10',
			'password': 'test',
			'date_start': (timezone.now() + timedelta(days=1)).isoformat(),
			'max_players': 14,
			'cost': 10,
			'price_1': 1000,
			'price_2': 500,
			'price_3': 250,
			'players': ['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test15', 'test18', 'test19', 'test20'], }
		self.base_json['status'] = 'success'
		self.base_json['message'] = 'Tournament created successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournament), json.dumps(
			self.tournament), content_type='application/json')
		self.check_json(response, 200)

		# Username is NOK
		self.invitation = {
			'username': 'test122',
			'password': 'test',
			'tournament_id': '1'
		}
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'The user does not exist'
		self.base_json['data'] = None
		response = self.client.post(reverse(accept_invitation), json.dumps(
			self.invitation), content_type='application/json')
		self.check_json(response, 400)

		# Tournament is NOK
		self.invitation = {
			'username': 'test1',
			'password': 'test',
			'tournament_id': '10'
		}
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'The tournament does not exist'
		self.base_json['data'] = None
		response = self.client.post(reverse(accept_invitation), json.dumps(
			self.invitation), content_type='application/json')
		self.check_json(response, 400)

		# Username not invited
		self.invitation = {
			'username': 'test12',
			'password': 'test',
			'tournament_id': '1'
		}
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'You have not been invited to this tournament'
		self.base_json['data'] = None
		response = self.client.post(reverse(accept_invitation), json.dumps(
			self.invitation), content_type='application/json')
		self.check_json(response, 400)
		
		# Username does not have enough points
		self.invitation = {
			'username': 'test7',
			'password': 'test',
			'tournament_id': '1'
		}
		current_user = User.objects.get(username = self.invitation['username'])
		current_user.puntos = 0
		current_user.save()
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'You do not have enough points to accept the invitation'
		self.base_json['data'] = None
		response = self.client.post(reverse(accept_invitation), json.dumps(
			self.invitation), content_type='application/json')
		self.check_json(response, 400)

	# Accept invitation is ok
		self.invitation = {
			'username': 'test2',
			'password': 'test',
			'tournament_id': '1'
		}
		self.base_json['status'] = 'success'
		self.base_json['message'] = 'Invitation accepted successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(accept_invitation), json.dumps(
			self.invitation), content_type='application/json')
		self.check_json(response, 200)
