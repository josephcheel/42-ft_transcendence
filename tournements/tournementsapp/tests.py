from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from tournementsapp.views import open_tournement
from datetime import datetime, timedelta
import json

# Create your tests here.
User = get_user_model()

# Create an array of users
class tournementTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.users = []
		self.users_creation_response = []
		for i in range(1, 22):
			self.users.append({'username': f"test{i}", 'password': "test"})
		self.base_json = {	'status': None, 'message': None, 'data': None }
	
	def check_json(self, response, code):
		self.assertJSONEqual(json.dumps(self.base_json), response.content.decode("utf-8"))
		self.assertEqual(response.status_code, code)

	def tournament_creation(self):
		for i in range(1, 22):
			User.objects.create(username=f"test{i}", password="test")
		self.tournament = Client()
		self.tournament = {
			'username': 'test55', 
			'date_start': datetime.now(), 
			'max_players': 16, 
			'cost': 100, 
			'price_1': 1000, 
			'price_2': 500,
			'price_3': 250, 
			'players':['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10'],}	
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'A user does not exist'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournement), json.dumps(self.tournament), content_type='application/json')
		print('respuesta')
		print(response.content)
		self.check_json(response, 404)

		self.tournament = {
			'username': 'test10', 
			'date_start': datetime.now() - timedelta(days=1), 
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
		print('respuesta')
		print(response.content)
		self.check_json(response, 400)

		self.tournament = {
			'username': 'test10', 
			'date_start': datetime.now() + timedelta(days=1), 
			'max_players': 15, 
			'cost': 100, 
			'price_1': 1000, 
			'price_2': 500,
			'price_3': 250,
			'players':['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10'],}	
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'Invalid start date'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournement), json.dumps(self.tournament), content_type='application/json')
		print('respuesta')
		print(response.content)
		self.check_json(response, 400)

		self.tournament = {
			'username': 'test10', 
			'date_start': datetime.now() + timedelta(days=1), 
			'max_players': 14, 
			'cost': -100, 
			'price_1': 1000, 
			'price_2': 500,
			'price_3': 250,
			'players':['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10'],}
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'Invalid start date'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournement), json.dumps(self.tournament), content_type='application/json')
		print('respuesta')
		print(response.content)
		self.check_json(response, 400)

		self.tournament = {
			'username': 'test10', 
			'date_start': datetime.now() + timedelta(days=1), 
			'max_players': 14, 
			'cost': 100, 
			'price_1': -1000, 
			'price_2': 500,
			'price_3': 250,
			'players':['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10'],}
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'Invalid start date'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournement), json.dumps(self.tournament), content_type='application/json')
		print('respuesta')
		print(response.content)
		self.check_json(response, 400)

		self.tournament = {
			'username': 'test10', 
			'date_start': datetime.now() + timedelta(days=1), 
			'max_players': 14, 
			'cost': 100, 
			'price_1': 1000, 
			'price_2': -500,
			'price_3': 250 }
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'Invalid start date'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournement), json.dumps(self.tournament), content_type='application/json')
		print('respuesta')
		print(response.content)
		self.check_json(response, 400)

		self.tournament = {
			'username': 'test10', 
			'date_start': datetime.now() + timedelta(days=1), 
			'max_players': 14, 
			'cost': 100, 
			'price_1': 1000, 
			'price_2': 500,
			'price_3': -250,
			'players':['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10'],}
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'Invalid start date'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournement), json.dumps(self.tournament), content_type='application/json')
		print('respuesta')
		print(response.content)
		self.check_json(response, 400)

		self.tournament = {
			'username': 'test10', 
			'date_start': datetime.now() + timedelta(days=1), 
			'max_players': 14, 
			'cost': 100, 
			'price_1': 1000, 
			'price_2': 500,
			'price_3': 250,
			'players':['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10'],}
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'Invalid start date'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournement), json.dumps(self.tournament), content_type='application/json')
		print('respuesta')
		print(response.content)
		self.check_json(response, 400)