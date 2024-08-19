from django.test import TestCase, Client
from django.urls import reverse
from .models import User
from .views import create_user
import json

class UserModelTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = {"username" : "test1", "password" : "test"}
        self.user2 = {"username" : "test2", "password" : "test"}
        self.base_json = {
            'status': None,
            'message': None,
            'data': None
        }

    def check_json(self, response, code):
        self.assertJSONEqual(json.dumps(self.base_json), response.content.decode("utf-8"))
        self.assertEqual(response.status_code, code)        

    def test_user_creation(self):
        self.base_json['status'] = 'success'
        self.base_json['message'] = 'User created successfully'
        self.base_json['data'] = {'id' : 1, 'username' : 'test1'}

        response = self.client.post(reverse(create_user),json.dumps(self.user1),content_type='application/json')

        self.check_json(response, 201)


        self.base_json['status'] = 'success'
        self.base_json['message'] = 'User created successfully'
        self.base_json['data'] = {'id' : 2, 'username' : 'test2'}

        response = self.client.post(reverse(create_user),json.dumps(self.user2),content_type='application/json')
        self.check_json(response, 201)


    def test_duplicate(self):
        self.base_json['status'] = 'error'
        self.base_json['message'] = 'User already Exists'
        self.base_json['data'] = None
        response = self.client.post(reverse(create_user),json.dumps(self.user1),content_type='application/json')
        response = self.client.post(reverse(create_user),json.dumps(self.user1),content_type='application/json')
        self.check_json(response, 409)

    def test_invalid_body(self):
        self.base_json['status'] = 'error'
        self.base_json['message'] = 'Invalid Json body'
        self.base_json['data'] = None
        response = self.client.post(reverse(create_user))
        self.check_json(response, 400)

    def test_no_user_password(self):
        self.base_json['status'] = 'error'
        self.base_json['message'] = 'Empty username or password'
        self.base_json['data'] = None
        response = self.client.post(reverse(create_user), json.dumps({'esto no es username' : 'nope', 'password': 'test'}), content_type='application/json')
        self.check_json(response, 400)
        response = self.client.post(reverse(create_user), json.dumps({'username' : 'hello', 'esto no es password': 'test'}), content_type='application/json')
        self.check_json(response, 400)

    def test_valid_method_only(self):
        self.base_json['status'] = 'error'
        self.base_json['message'] = 'Invalid request method'
        self.base_json['data'] = None
        response = self.client.get(reverse(create_user))
        self.check_json(response, 400)

