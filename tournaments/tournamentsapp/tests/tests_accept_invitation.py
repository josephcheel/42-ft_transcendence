from tournamentsapp.models import Tournaments, Invitations, Matches, User
from django.test import TestCase, Client
from django.urls import reverse
from tournamentsapp.views.open_tournament import open_tournament
from tournamentsapp.views.accept_invitation import accept_invitation
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
			current_user = User.objects.create_user(username=f"test{i}", password="test")

	def check_json(self, response, code):
		self.assertJSONEqual(json.dumps(self.base_json),
		                     response.content.decode("utf-8"))
		self.assertEqual(response.status_code, code)

	def test_accept_invitation(self):
		self.client.login(username="test10", password="test")
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

#		# Username is NOK
#		self.invitation = {
#			'username': 'test122',
#			'password': 'test',
#			'tournament_id': '1'
#		}
#		self.base_json['status'] = 'error'
#		self.base_json['message'] = 'User not authenticated'
#		self.base_json['data'] = None
#		response = self.client.post(reverse(accept_invitation), json.dumps(
#			self.invitation), content_type='application/json')
#		self.check_json(response, 405)

		# Tournament is NOK
		self.invitation = {
			'tournament_id': '10'
		}
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'The tournament does not exist'
		self.base_json['data'] = None
		response = self.client.post(reverse(accept_invitation), json.dumps(
			self.invitation), content_type='application/json')
		self.check_json(response, 400)

		# Username not invited
		self.client.logout()
		self.client.login(username="test12", password="test")
		self.invitation = {
			'tournament_id': '1'
		}
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'You have not been invited to this tournament'
		self.base_json['data'] = None
		response = self.client.post(reverse(accept_invitation), json.dumps(
			self.invitation), content_type='application/json')
		self.check_json(response, 400)
		
		# Username does not have enough points
		self.client.logout()
		self.client.login(username="test7", password="test")
		self.invitation = {
			'tournament_id': '1'
		}
		current_user = User.objects.get(username = 'test7')
		current_user.puntos = 0
		current_user.save()
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'You do not have enough points to accept the invitation'
		self.base_json['data'] = None
		response = self.client.post(reverse(accept_invitation), json.dumps(
			self.invitation), content_type='application/json')
		self.check_json(response, 400)

	# Accept invitation is ok
		self.client.logout()
		self.client.login(username="test2", password="test")
		self.invitation = {
			'tournament_id': '1'
		}
		self.base_json['status'] = 'success'
		self.base_json['message'] = 'Invitation accepted successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(accept_invitation), json.dumps(
			self.invitation), content_type='application/json')
		self.check_json(response, 200)
