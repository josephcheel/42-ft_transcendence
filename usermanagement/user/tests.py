from django.test import TestCase, Client
from django.urls import reverse
from .views import create_user, login_user, is_logged_in, logout_user, list_users, user_status, send_friend_request
import json
from django.db import OperationalError
from django.contrib.auth import get_user_model, login, logout
from .models import UserStatus, Friendship

User = get_user_model()




class usermodelTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = {"username" : "Test1", "password" : "test"}
        self.user2 = {"username" : "Test2", "password" : "test"}
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
        self.base_json['data'] = {'id' : 1, 'username' : self.user1['username']}

        response = self.client.post(reverse(create_user),json.dumps(self.user1),content_type='application/json')

        self.check_json(response, 201)

        user = User.objects.get(username=self.user1['username'].lower())
        self.assertEqual(user.original_username, self.user1['username'])


        self.base_json['status'] = 'success'
        self.base_json['message'] = 'User created successfully'
        self.base_json['data'] = {'id' : 2, 'username' : self.user2['username']}

        response = self.client.post(reverse(create_user),json.dumps(self.user2),content_type='application/json')
        self.check_json(response, 201)
    

    def test_duplicate(self):
        self.base_json['status'] = 'error'
        self.base_json['message'] = 'User already Exists'
        self.base_json['data'] = None
        response = self.client.post(reverse(create_user),json.dumps(self.user1),content_type='application/json')
        response = self.client.post(reverse(create_user),json.dumps(self.user1),content_type='application/json')
        self.check_json(response, 409)
        response = self.client.post(reverse(create_user),json.dumps({'username' : self.user1['username'].upper(), 'password': self.user1['password']}),content_type='application/json')
        self.check_json(response, 409)


    def test_invalid_body(self):
        self.base_json['status'] = 'error'
        self.base_json['message'] = 'Invalid JSON body'
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
        self.base_json['message'] = 'Invalid request method, POST required'
        self.base_json['data'] = None
        response = self.client.get(reverse(create_user))
        self.check_json(response, 405)

    def test_get_all_users(self):
        self.base_json['status'] = 'success'
        self.base_json['message'] = 'All registered users'
        self.base_json['data'] = []

        response = self.client.get(reverse(list_users))
        self.check_json(response, 200)
        self.base_json['data'] = [{'id': 1, 'username': self.user1['username'].lower()}]
        response = self.client.post(reverse(create_user),json.dumps(self.user1),content_type='application/json')
        response = self.client.get(reverse(list_users))
        self.check_json(response, 200)


class logInTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = {"username" : "test1", "password" : "test"}
        self.base_json = {
            'status': None,
            'message': None,
            'data': None
        }
        self.client.post(reverse(create_user),json.dumps(self.user1),content_type='application/json')

    def check_json(self, response, code):
        self.assertJSONEqual(json.dumps(self.base_json), response.content.decode("utf-8"))
        self.assertEqual(response.status_code, code)      


    def test_login_user(self):
        self.base_json['status'] = 'success'
        self.base_json['message'] = 'user is logged in'
        self.base_json['data'] = None

        response = self.client.post(reverse(login_user), json.dumps(self.user1),content_type='application/json')
        self.check_json(response, 200)
        self.assertTrue(self.client.session['_auth_user_id'], 'User ID should be present in session')

    def test_invalid_login_user(self):

        self.base_json['status'] = 'error'
        self.base_json['message'] = 'Invalid credentials'
        self.base_json['data'] = None
        #incorrect Password
        response = self.client.post(reverse(login_user), json.dumps({'username' : self.user1['username'], 'password': 'contrasincorrecta'}),content_type='application/json')
        self.check_json(response, 401)
        self.assertNotIn('_auth_user_id', self.client.session, 'User ID should not be present in session')
        #incorrect user
        response = self.client.post(reverse(login_user), json.dumps({'username' : 'usuario no existe', 'password': self.user1['password']}),content_type='application/json')
        self.check_json(response, 401)
        self.assertNotIn('_auth_user_id', self.client.session, 'User ID should not be present in session')
        #incorrect user and password
        response = self.client.post(reverse(login_user), json.dumps({'username' : 'usuario no existe', 'password': 'contranoexiste'}),content_type='application/json')
        self.check_json(response, 401)
        self.assertNotIn('_auth_user_id', self.client.session, 'User ID should not be present in session')

    def test_no_user_password(self):
        self.base_json['status'] = 'error'
        self.base_json['message'] = 'Empty username or password'
        self.base_json['data'] = None
        #missing username field
        response = self.client.post(reverse(login_user), json.dumps({'esto no es username' : 'nope', 'password': 'test'}), content_type='application/json')
        self.check_json(response, 400)
        #missing password field
        response = self.client.post(reverse(login_user), json.dumps({'username' : 'hello', 'esto no es password': 'test'}), content_type='application/json')
        self.check_json(response, 400)
        #missing password and username field
        response = self.client.post(reverse(login_user), json.dumps({'username' : 'hello', 'esto no es password': 'test'}), content_type='application/json')
        self.check_json(response, 400)

    def test_user_is_logged_in(self):
        self.base_json['status'] = 'success'
        self.base_json['message'] = 'User is logged in'
        self.base_json['data'] = None

        self.client.login(username=self.user1['username'], password=self.user1['password'])
        response = self.client.get(reverse(is_logged_in))
        self.check_json(response, 200)

    def test_user_is_not_logged_in(self):
        self.client.logout()
        self.base_json['status'] = 'error'
        self.base_json['message'] = 'Unauthorized'
        self.base_json['data'] = None
        response = self.client.get(reverse(is_logged_in))
        self.check_json(response, 401)


    def test_logout_success(self):
        self.client.login(username=self.user1['username'], password=self.user1['password'])
        response = self.client.post(reverse(logout_user))
        
        self.base_json['status'] = 'success'
        self.base_json['message'] = 'user has been logged out'
        self.base_json['data'] = None

        self.assertNotIn('_auth_user_id', self.client.session)
        self.check_json(response, 200)


    def test_logout_without_login(self):
        response = self.client.post(reverse(logout_user))

        self.base_json['status'] = 'error'
        self.base_json['message'] = 'Forbidden'
        self.base_json['data'] = None

        self.check_json(response, 403)


class userStatusTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = {"username" : "test1", "password" : "test"}
        self.base_json = {
            'status': None,
            'message': None,
            'data': None
        }
        self.client.post(reverse(create_user),json.dumps(self.user1),content_type='application/json')
        self.user = User.objects.get(username=self.user1['username'])

    def check_json(self, response, code):
        self.assertJSONEqual(json.dumps(self.base_json), response.content.decode("utf-8"))
        self.assertEqual(response.status_code, code)

    def test_is_online_after_login(self):
        self.client.post(reverse(login_user),json.dumps(self.user1),content_type='application/json')
        user_status = UserStatus.objects.get(user=self.user)
        self.assertTrue(user_status.is_online)

    def test_is_offline_after_logout(self):
        user_status = UserStatus.objects.get(user=self.user)
        self.client.post(reverse(logout_user),json.dumps(self.user1),content_type='application/json')
        self.assertFalse(user_status.is_online)


    def test_get_user_status(self):

        self.base_json['status'] = 'success'
        self.base_json['message'] = 'Retrieved status'
        self.base_json['data'] = {'is_online' : True}

        self.client.post(reverse(login_user),json.dumps(self.user1),content_type='application/json')
        response = self.client.get(reverse(user_status),{'username': self.user1['username']})
        user_status_ = UserStatus.objects.get(user=self.user)
        self.check_json(response, 200)
        self.assertTrue(user_status_.is_online)

        self.base_json['data'] = {'is_online' : False}

        self.client.post(reverse(logout_user),json.dumps(self.user1),content_type='application/json')
        response = self.client.get(reverse(user_status),{'username': self.user1['username']})
        user_status_ = UserStatus.objects.get(user=self.user)
        self.check_json(response, 200)
        self.assertFalse(user_status_.is_online)
      
    def test_post_user_status(self):

        self.base_json['status'] = 'success'
        self.base_json['message'] = 'Updated status'
        self.base_json['data'] = None

        self.client.post(reverse(login_user),json.dumps(self.user1),content_type='application/json')


        response = self.client.post(reverse(user_status),json.dumps({'status':'online'}),content_type='application/json')
        user_status_ = UserStatus.objects.get(user=self.user)
        self.check_json(response, 200)
        self.assertTrue(user_status_.is_online)

        response = self.client.post(reverse(user_status),json.dumps({'status':'offline'}),content_type='application/json')

        user_status_ = UserStatus.objects.get(user=self.user)
        self.check_json(response, 200)
        self.assertFalse(user_status_.is_online)

class friendShipTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='test1', password='test')
        self.user2 = User.objects.create_user(username='test2', password='test')

        self.client.login(username='test1', password='test')
        self.friend = {'username' : 'test2'}
        self.base_json = {
            'status': None,
            'message': None,
            'data': None
        }

        
    def login_user(self, username, password):
        # Log in as user1
        self.client.login(username=username, password=password)

    def logout_user(self):
        # Log out the currently logged in user
        self.client.logout()

    def create_friendship(self):
        friends = Friendship()
        friends.save()
        friends.users.add(self.user1, self.user2)

    def check_json(self, response, code):
        self.assertJSONEqual(json.dumps(self.base_json), response.content.decode("utf-8"))
        self.assertEqual(response.status_code, code)

    def test_not_auth(self):
        self.logout_user()
        self.base_json['status'] = 'error'
        self.base_json['message'] = 'Invalid credentials'
        self.base_json['data'] = None

        response = self.client.post(reverse(send_friend_request), json.dumps(self.friend),content_type='application/json' )
        self.check_json(response, 401)

    def test_no_friend_sent(self):
        self.base_json['status'] = 'error'
        self.base_json['message'] = 'Empty username'
        self.base_json['data'] = None

        response = self.client.post(reverse(send_friend_request), json.dumps({'nothing' : 'nothing'}),content_type='application/json' )
        self.check_json(response, 400)

    def test_success_create(self):
        self.login_user('test1', 'test')
        self.base_json['status'] = 'success'
        self.base_json['message'] = 'Friendship created'
        self.base_json['data'] = None

        response = self.client.post(reverse(send_friend_request), json.dumps({'username' : 'Test2'}),content_type='application/json' )
        self.check_json(response, 201)


    def test_already_friends(self):
        self.create_friendship()
        self.login_user('test1', 'test')
        self.base_json['status'] = 'error'
        self.base_json['message'] = 'Users are already friends'
        self.base_json['data'] = None

        response = self.client.post(reverse(send_friend_request), json.dumps({'username' : 'Test2'}),content_type='application/json' )
        self.check_json(response, 400)


    def test_friend_doesnot_exist(self):
        self.login_user('test1', 'test')
        self.base_json['status'] = 'error'
        self.base_json['message'] = 'User does not exists'
        self.base_json['data'] = None

        response = self.client.post(reverse(send_friend_request), json.dumps({'username' : 'no_existo'}),content_type='application/json' )
        self.check_json(response, 404)