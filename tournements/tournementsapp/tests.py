from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .views import open_tournement, accept_invitation
from datetime import timedelta
from django.utils import timezone
from django.db import OperationalError
import json

# Create your tests here.
User = get_user_model()

# Create an array of users
class test_open_tournement(TestCase):
	def setUp(self):
		self.client = Client()
		self.users = []
		for i in range(1, 22):
			self.users.append({'username': f"test{i}", 'password': "test"})
		self.base_json = {	'status': None, 'message': None, 'data': None }
	
	def check_json(self, response, code):
		self.assertJSONEqual(json.dumps(self.base_json), response.content.decode("utf-8"))
		self.assertEqual(response.status_code, code)

	def test_tournament_creation(self):
		for i in range(1, 22):
			User.objects.create(username=f"test{i}", password="test")
		self.tournament = Client()

		#Owner does not exist
		self.tournament = {
			'username': 'test55', 
			'max_players': 16, 
			'date_start': (timezone.now() + timedelta(days=1)).isoformat(), 
			'cost': 100, 
			'price_1': 1000, 
			'price_2': 500,
			'price_3': 250, 
			'players':['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10'],}	
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'The owner user does not exist'
		self.base_json['data'] = None
		response = self.client.post(
			'/tournements/open/', json.dumps(self.tournament), content_type='application/json')
		self.check_json(response, 400)

		#Invalid start date
		self.tournament = {
			'username': 'test10', 
			'date_start': (timezone.now() - timedelta(days=1)).isoformat(), 
			'max_players': 16, 
			'cost': 100, 
			'price_1': 1000, 
			'price_2': 500,
			'price_3': 250,
			'players':['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10'],}	
		self.base_json['status'] = 'error'
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'Invalid start date'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournement), json.dumps(self.tournament), content_type='application/json')
		self.check_json(response, 400)

		#Max players must be even
		self.tournament = {
			'username': 'test10', 
			'date_start': (timezone.now() + timedelta(days=1)).isoformat(),
			'max_players': 15, 
			'cost': 100, 
			'price_1': 1000, 
			'price_2': 500,
			'price_3': 250,
			'players':['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10'],}	
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'The max number of players must be even'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournement), json.dumps(self.tournament), content_type='application/json')
		self.check_json(response, 400)

		#Cost or cost must be positive
		self.tournament = {
			'username': 'test10', 
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
		response = self.client.post(reverse(open_tournement), json.dumps(self.tournament), content_type='application/json')
		self.check_json(response, 400)

		# Prices or cost must be positive
		self.tournament = {
			'username': 'test10', 
			'date_start': (timezone.now() + timedelta(days=1)).isoformat(),
			'max_players': 14, 
			'cost': 100, 
			'price_1': -1000, 
			'price_2': 500,
			'price_3': 250,
			'players':['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10'],}
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'Prices or cost must be positive'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournement), json.dumps(self.tournament), content_type='application/json')
		self.check_json(response, 400)

		# Prices or cost must be positive
		self.tournament = {
			'username': 'test10', 
			'date_start': (timezone.now() + timedelta(days=1)).isoformat(),
			'max_players': 14, 
			'cost': 100, 
			'price_1': 1000, 
			'price_2': -500,
			'price_3': 250 }
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'Prices or cost must be positive'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournement), json.dumps(self.tournament), content_type='application/json')
		self.check_json(response, 400)

		# Prices or cost must be positive
		self.tournament = {
			'username': 'test10', 
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
		response = self.client.post(reverse(open_tournement), json.dumps(self.tournament), content_type='application/json')
		self.check_json(response, 400)

		# All players invited must exist
		self.tournament = {
			'username': 'test10',
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
		response = self.client.post(reverse(open_tournement), json.dumps(
			self.tournament), content_type='application/json')
		self.check_json(response, 400)

		# Everithing is ok
		self.tournament = {
			'username': 'test10',
			'date_start': (timezone.now() + timedelta(days=1)).isoformat(),
			'max_players': 14,
			'cost': 100,
			'price_1': 1000,
			'price_2': 500,
			'price_3': 250,
			'players': ['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10'], }
		self.base_json['status'] = 'success'
		self.base_json['message'] = 'Tournement created successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournement), json.dumps(
			self.tournament), content_type='application/json')
		self.check_json(response, 200)

class test_accept_invitation (TestCase):
	def setUp(self):
		self.client = Client()
		self.users = []
		for i in range(1, 22):
			self.users.append({'username': f"test{i}", 'password': "test"})
		self.base_json = {	'status': None, 'message': None, 'data': None }
		self.tournament = {
			'username': 'test10',
			'date_start': (timezone.now() + timedelta(days=1)).isoformat(),
			'max_players': 14,
			'cost': 100,
			'price_1': 1000,
			'price_2': 500,
			'price_3': 250,
			'players': ['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10'], }
		response = self.client.post(reverse(open_tournement), json.dumps(
			self.tournament), content_type='application/json')

	def check_json(self, response, code):
		self.assertJSONEqual(json.dumps(self.base_json),
		                     response.content.decode("utf-8"))
		self.assertEqual(response.status_code, code)

	# Accept invitation is ok
	def test_accept_invitation(self):
		self.invitation = {
			'username': 'test11',
			'tournament': '1'
		}
		self.base_json['status'] = 'success'
		self.base_json['message'] = 'Invitation accepted'
		self.base_json['data'] = None
		response = self.client.post(reverse(accept_invitation), json.dumps(self.invitation), content_type='application/json')
		self.check_json(response, 200)