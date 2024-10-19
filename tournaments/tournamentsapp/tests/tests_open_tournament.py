from tournamentsapp.models import Tournaments, Invitations, Matches, User
from django.test import TestCase, Client
from django.urls import reverse
from tournamentsapp.views.open_tournament import open_tournament
from datetime import timedelta
from django.utils import timezone
from django.db import OperationalError
import json
from tournamentsapp.status_options import StatusTournaments, StatusInvitations, StatusMatches, Rounds
import random
from .printing import print_all_tournaments, print_all_invitations, print_all_matches, print_all_users
from datetime import datetime
# Create your tests here.
from django.contrib.auth import get_user_model
User = get_user_model()

# Create an array of users
class test_open_tournament(TestCase):
	def setUp(self):
		self.client = Client()
		for i in range(1, 22):
			current_user = User.objects.create_user(username=f"test{i}", password="test")
		self.base_json = {'status': None, 'message': None, 'data': None}
	
	def check_json(self, response, code):
		self.assertJSONEqual(json.dumps(self.base_json), response.content.decode("utf-8"))
		self.assertEqual(response.status_code, code)

	def test_tournament_creation(self):
		self.tournament = Client()

		#Owner does not exist
		self.tournament = {
			'username': 'test55', 
			'password': 'test',
			'max_players': 16,
			'date_start': (timezone.now() + timedelta(days=1)).isoformat(), 
			'cost': 10, 
			'price_1': 1000, 
			'price_2': 500,
			'price_3': 250, 
			'players':['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10'],}	
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'User not authenticated'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournament), json.dumps(self.tournament), content_type='application/json')
		self.check_json(response, 405)

		#Invalid start date
		user = User.objects.get(username='test10')
		success = self.client.login(username="test10", password="test")
		self.assertTrue(success, "Login failed")
		self.tournament = {
			'username': 'test10', 
			'password': 'test',
			'date_start': (timezone.now() - timedelta(days=1)).isoformat(),
			'max_players': 16, 
			'cost': 10, 
			'price_1': 1000, 
			'price_2': 500,
			'price_3': 250,
			'players':['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10'],}	
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'Invalid start date'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournament), json.dumps(self.tournament), content_type='application/json')
		self.check_json(response, 400)

#		#Max players must be even
#		self.tournament = {
#			'username': 'test10', 
#			'password': 'test',
#			'date_start': (timezone.now() + timedelta(days=1)).isoformat(),
#			'max_players': 15, 
#			'cost': 100, 
#			'price_1': 1000, 
#			'price_2': 500,
#			'price_3': 250,
#			'players':['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10'],}	
#		self.base_json['status'] = 'error'
#		self.base_json['message'] = 'The max number of players must be even'
#		self.base_json['data'] = None
#		response = self.client.post(reverse(open_tournament), json.dumps(self.tournament),content_type='application/json')
#		self.check_json(response, 400)

		#Cost or cost must be positive
		self.tournament = {
			'username': 'test10', 
			'password': 'test',
			'date_start': (timezone.now() + timedelta(days=1)).isoformat(),
			'max_players': 14, 
			'cost': -100, 
			'price_1': 1000, 
			'price_2': 500,
			'price_3': 250,
			'players':['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10'],}
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'Prices or cost must be positive'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournament), json.dumps(self.tournament), content_type='application/json')
		self.check_json(response, 400)

		# Prices or cost must be positive
		self.tournament = {
			'username': 'test10', 
			'password': 'test',
			'date_start': (timezone.now() + timedelta(days=1)).isoformat(),
			'max_players': 14, 
			'cost': 10, 
			'price_1': -1000, 
			'price_2': 500,
			'price_3': 250,
			'players':['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10'],}
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'Prices or cost must be positive'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournament), json.dumps(self.tournament), content_type='application/json')
		self.check_json(response, 400)

		# Prices or cost must be positive
		self.tournament = {
			'username': 'test10', 
			'password': 'test',
			'date_start': (timezone.now() + timedelta(days=1)).isoformat(),
			'max_players': 14, 
			'cost': 100, 
			'price_1': 1000, 
			'price_2': -500,
			'price_3': 250 }
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'Prices or cost must be positive'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournament), json.dumps(self.tournament), content_type='application/json')
		self.check_json(response, 400)

		# Prices or cost must be positive
		self.tournament = {
			'username': 'test10', 
			'password': 'test',
			'date_start': (timezone.now() + timedelta(days=1)).isoformat(),
			'max_players': 14, 
			'cost': 100, 
			'price_1': 1000, 
			'price_2': 500,
			'price_3': -250,
			'players':['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10'],}
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'Prices or cost must be positive'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournament), json.dumps(self.tournament), content_type='application/json')
		self.check_json(response, 400)

		# All players invited must exist
		self.tournament = {
			'username': 'test10',
			'password': 'test',
			'date_start': (timezone.now() + timedelta(days=1)).isoformat(),
			'max_players': 14,
			'cost': 100,
			'price_1': 1000,
			'price_2': 500,
			'price_3': 250,
			'players': ['test111', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10'], }
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'One invited player does not exist'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournament), json.dumps(
			self.tournament), content_type='application/json')
		self.check_json(response, 400)

		# Everithing is ok
		self.tournament = {
			'username': 'test10',
			'password': 'test',
			'date_start': (timezone.now() + timedelta(days=1)).isoformat(),
			'max_players': 14,
			'cost': 10,
			'price_1': 1000,
			'price_2': 500,
			'price_3': 250,
			'players': ['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10'], }
		self.base_json['status'] = 'success'
		self.base_json['message'] = 'Tournament created successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournament), json.dumps(
			self.tournament), content_type='application/json')
		self.check_json(response, 200)
