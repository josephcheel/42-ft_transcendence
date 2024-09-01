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
		for i in range(1, 22):
			self.users_creation_response.append({'id': i, 'username': f"test{i}"})
		for user in self.users:
			print(user)
		self.base_json = {	'status': None, 'message': None, 'data': None }
	
	def check_json(self, response, code):
		self.assertJSONEqual(json.dumps(self.base_json), response.content.decode("utf-8"))
		self.assertEqual(response.status_code, code)

	def test_user_creation(self):
		for i in range(1, 22):
			user = self.users[i-1]
			user_cration_response = self.users_creation_response
			self.base_json['status'] = 'success'
			self.base_json['message'] = 'User created successfully'
			self.base_json['data'] = user_cration_response
			response = self.client.post('user/create_user', json.dumps(user), content_type='application/json')
			print(response)
			self.check_json(response, 201)
		list_of_users = User.objects.all()
		for user in list_of_users:
			print("user= ", user.username, "- password= ", user.password)