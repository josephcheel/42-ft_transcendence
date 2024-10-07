from django.test import TestCase
import json
import requests

# Create your tests here.
USERMANAGEMENT_URL = "http://usermanagement:8000/user/create_user/"

class test_accept_invitation (TestCase):
	def setUp(self):
		#self.client = Client()
		self.users = []

	def check_json(self, response, code):
		self.assertJSONEqual(json.dumps(self.base_json),
		                     response.content.decode("utf-8"))
		self.assertEqual(response.status_code, code)

	def test_create_user(self):
		response = requests.post(USERMANAGEMENT_URL, json.dumps(
			{'username': 'test1', 'password': 'test', 'first_name': 'test', 'last_name': 'test'}), headers={'Content-Type': 'application/json'})
		self.base_json = {'status': None, 'message': None, 'data': None}
		self.base_json['status'] = 'success'
		self.base_json['message'] = 'User created successfully'
		self.base_json['data'] = None
		print("The response content is:")
		print(response.content)
#		self.check_json(response, 201)
