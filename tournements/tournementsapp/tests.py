from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
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
		self.turnement = Client()
		self.turnement = {'username': 'test55', 'date_start': '2021-07-01 00:00:00', 'max_players': 16, 'cost': 100, 'price_1': 1000, 'price_2': 500, 'price_3': 250 }
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'A user does not exist'
		self.base_json['data'] = None
		response = self.client.post(reverse(create_tournament), json.dumps(self.turnement), content_type='application/json')
		print('respuesta')
		print(response.content)
		self.check_json(response, 404)
