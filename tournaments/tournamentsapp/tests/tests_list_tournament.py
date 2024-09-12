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

# Create an array of users
class test_list_tournaments(TestCase):

	def setUp(self):
		self.client = Client()
		self.users = []
		for i in range(1, 22):
			current_user = User.objects.create(username=f"test{i}", password="test")
		self.base_json = {'status': None, 'message': None, 'data': None}
	
	def check_json(self, response, code):
		self.assertJSONEqual(json.dumps(self.base_json), response.content.decode("utf-8"))
		self.assertEqual(response.status_code, code)

	def test_list_tournaments(self):
		self.tournament = {
			'username': 'test10',
			'password': 'test',
			'date_start': (timezone.now() + timedelta(days=1)).isoformat(),
			'max_players': 14,
			'cost': 10,
			'price_1': 1000,
			'price_2': 500,
			'price_3': 250,
			'players': ['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11', 'test12'], }
		self.base_json['status'] = 'success'
		self.base_json['message'] = 'Tournament created successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournament), json.dumps(
			self.tournament), content_type='application/json')
		self.check_json(response, 200)
		self.tournament = {
			'username': 'test10',
			'password': 'test',
			'date_start': (timezone.now() + timedelta(days=1)).isoformat(),
			'max_players': 14,
			'cost': 10,
			'price_1': 1000,
			'price_2': 500,
			'price_3': 250,
			'players': ['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11', 'test12'], }
		self.base_json['status'] = 'success'
		self.base_json['message'] = 'Tournament created successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournament), json.dumps(
			self.tournament), content_type='application/json')
		self.check_json(response, 200)

		self.tournament = {
			'username': 'test10',
			'password': 'test',
			'date_start': (timezone.now() + timedelta(days=1)).isoformat(),
			'max_players': 14,
			'cost': 10,
			'price_1': 1000,
			'price_2': 500,
			'price_3': 250,
			'players': ['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11', 'test12'], }
		self.base_json['status'] = 'success'
		self.base_json['message'] = 'Tournament created successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournament), json.dumps(
			self.tournament), content_type='application/json')
		self.check_json(response, 200)

		self.list_tournaments = {
			'username': 'test10',
			'password': 'test'}
		owner = User.objects.get(username='test10')
		tournament_data = Tournaments.objects.filter(player_id=owner.id)

		# Convert any datetime fields to string
		tournament_list = list(tournament_data.values())
		for tournament in tournament_list:
			for key, value in tournament.items():
				if isinstance(value, datetime):
					tournament[key] = value.isoformat()
		self.base_json['status'] = 'success'
		self.base_json['message'] = 'List of tournaments cereated'
		self.base_json['data'] = json.dumps(tournament_list)
		print (self.base_json['data'])
		url = reverse(list_tournaments)
		print (url)
		response = self.client.get(reverse(list_tournaments), json.dumps(
			self.list_tournaments), content_type='application/json')
		print(response.content.decode("utf-8"))	
		self.check_json(response, 200)
