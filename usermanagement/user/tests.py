from django.test import TestCase, Client, override_settings
from django.urls import reverse
from .views import *
import json
from django.db import OperationalError
from django.contrib.auth import get_user_model
from .models import UserStatus, Friendship, User
import os
from django.conf import settings

class usermodelTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = {'first_name': 'Luis', 'last_name' : 'Soto', "username" : "Test1", "password" : "test"}
        self.user2 = {'first_name': 'Luis', 'last_name' : 'Soto', "username" : "Test2", "password" : "test"}
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
        self.base_json['data'] = None

        response = self.client.post(reverse(create_user),json.dumps(self.user1),content_type='application/json')

        self.check_json(response, 201)

        user = User.objects.get(username=self.user1['username'])
        self.assertEqual(user.username, self.user1['username'])


        self.base_json['status'] = 'success'
        self.base_json['message'] = 'User created successfully'
        self.base_json['data'] = None

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
        self.base_json['message'] = 'Invalid JSON body'
        self.base_json['data'] = None
        response = self.client.post(reverse(create_user))
        self.check_json(response, 400)

    def test_no_user_password(self):
        self.base_json['status'] = 'error'
        self.base_json['message'] = 'Missing required fields'
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
        self.base_json['data'] = [{'id': 1, 'username': self.user1['username']}]
        response = self.client.post(reverse(create_user),json.dumps(self.user1),content_type='application/json')
        response = self.client.get(reverse(list_users))
        self.check_json(response, 200)

class logInTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = {'first_name': 'Luis', 'last_name' : 'Soto', "username" : "test1", "password" : "test"}
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
        self.base_json['message'] = 'Missing required fields'
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
        self.base_json['data'] = {'id': 1, 'username': 'test1'}

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
        self.user1 = {'first_name': 'Luis', 'last_name' : 'Soto', "username" : "test1", "password" : "test",'tournament_name' : 'my_tournament_name'}
        self.base_json = {
            'status': None,
            'message': None,
            'data': None
        }
        self.client.post(reverse(create_user),json.dumps(self.user1),content_type='application/json')
        self.user = User.objects.get(username=self.user1['username'])
        self.client.login(username='test1', password='test')

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
        self.base_json['data'] = {'is_online' : False}

        response = self.client.get(reverse(user_status),{'username': self.user1['username']})
        user_status_ = UserStatus.objects.get(user=self.user)
        self.check_json(response, 200)
        self.assertFalse(user_status_.is_online)

        self.base_json['data'] = {'is_online' : False}

        self.client.post(reverse(logout_user),json.dumps(self.user1),content_type='application/json')
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

class changeFriendShipStatusTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='test1', password='test')
        self.user2 = User.objects.create_user(username='test2', password='test')
        self.user3 = User.objects.create_user(username='test3', password='test')
        self.client.login(username='test1', password='test')
        Friendship.add_friendship(self.user1, self.user2)
        self.friend = 'test2'
        self.status = 'accepted'
        self.base_json = {
            'status': None,
            'message': None,
            'data': None
        }
        self.response = None
        self.code = 200

    def login_user(self, username, password):
        # Log in as user1
        self.client.login(username=username, password=password)

    def check_json(self):
        self.assertJSONEqual(json.dumps(self.base_json), self.response.content.decode("utf-8"))
        self.assertEqual(self.response.status_code, self.code)
    
    def send_request(self):
        self.response = self.client.post(reverse(change_friendship_status), json.dumps({'username' : self.friend, 'status' : self.status}),content_type='application/json' )


    def test_not_valid_status(self):
        self.base_json['status'] = 'error'
        self.base_json['message'] = 'Invalid status'
        self.base_json['data'] = None
        self.status = 'Invalid' 
        self.send_request()
        self.code = 400        
        self.check_json()

        self.status = 'pending' 
        self.send_request()
        self.code = 400        
        self.check_json()

    def test_not_friendship(self):
        self.base_json['status'] = 'error'
        self.base_json['message'] = 'Users have no friendship'
        self.base_json['data'] = None

        self.friend = 'test3' 
        self.send_request()
        self.code = 404        
        self.check_json()
    
    def test_user_not_exists(self):
        self.base_json['status'] = 'error'
        self.base_json['message'] = 'User does not exists'
        self.base_json['data'] = None

        self.friend = 'no_existo' 
        self.send_request()
        self.code = 404        
        self.check_json()

    def test_success(self):
        self.base_json['status'] = 'success'
        self.base_json['message'] = 'Friendship modified'
        self.base_json['data'] = None
        self.code = 200        
        self.friend = 'test2' 
        
        ## Test change to accepted
        self.send_request()
        self.check_json()
        friendship = Friendship.get_friendship(self.user1, self.user2)
        self.assertEqual(friendship.first().status, 1)
        self.assertEqual(friendship.last().status, 1)


        friendship = Friendship.get_friendship(self.user2, self.user1)
        self.assertEqual(friendship.first().status, 1)
        self.assertEqual(friendship.last().status, 1)

        # Test change to declined

        self.status = 'declined'


        self.send_request()
        self.check_json()
        friendship = Friendship.get_friendship(self.user1, self.user2)
        self.assertEqual(friendship.first().status, 0)
        self.assertEqual(friendship.last().status, 0)


        friendship = Friendship.get_friendship(self.user2, self.user1)
        self.assertEqual(friendship.first().status, 0)
        self.assertEqual(friendship.last().status, 0)

class getAllFriends(TestCase):

    def setUp(self):
        self.client = Client()
        self.client2 = Client()
        self.client3 = Client()
        self.user1 = User.objects.create_user(lowercase_username='test1',username='Test1', password='test')
        self.user2 = User.objects.create_user(lowercase_username='test2',username='Test2', password='test')
        self.user3 = User.objects.create_user(lowercase_username='test3',username='Test3', password='test')

        #Create user Status state
        self.user1.userstatus.is_online = True
        self.user1.userstatus.save()
        self.client.login(username='Test1', password='test')
        self.client2.login(username='Test2', password='test')
        self.client3.login(username='Test3', password='test')
        Friendship.add_friendship(self.user1, self.user2)
        self.status = 'accepted'
        self.base_json = {
            'status': None,
            'message': None,
            'data': None
        }
        self.response = None
        self.code = 200


    def check_json(self):
        self.assertJSONEqual(json.dumps(self.base_json), self.response.content.decode("utf-8"))
        self.assertEqual(self.response.status_code, self.code)
    
    def send_request(self, client):
        self.response = client.get(reverse(get_friends))


    def test_valid(self):
        self.base_json['status'] = 'success'
        self.base_json['message'] = 'Got all friends'
        self.base_json['data'] = [{'friendship': 'pending', 'username': 'Test2', 'is_online': False}]
        self.send_request(self.client)
        self.code = 200        
        self.check_json()

        self.send_request(self.client2)
        self.base_json['data'] = [{'friendship': 'pending', 'username': 'Test1', 'is_online': True}]

        self.check_json()

    def test_valid_multiple_friends(self):
        Friendship.add_friendship(self.user1, self.user3)
        self.base_json['status'] = 'success'
        self.base_json['message'] = 'Got all friends'
        self.base_json['data'] = [{'friendship': 'pending', 'username': 'Test2', 'is_online': False}, 
                                  {'friendship': 'pending', 'username': 'Test3', 'is_online': False}]
        self.send_request(self.client)
        self.code = 200        
        self.check_json()

        self.send_request(self.client2)
        self.base_json['data'] = [{'friendship': 'pending', 'username': 'Test1', 'is_online': True}]

        self.check_json()
        
        self.send_request(self.client3)
        self.base_json['data'] = [{'friendship': 'pending', 'username': 'Test1', 'is_online': True}]

        self.check_json()

    def test_no_friends(self):
        self.base_json['status'] = 'success'
        self.base_json['message'] = 'Got all friends'
        self.base_json['data'] = []
        self.send_request(self.client3)
        self.check_json()

class updateUser(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='Test1',lowercase_username='test1', password='test')
        self.content = {}
        self.client.login(username='Test1', password='test')
        self.base_json = {
            'status': None,
            'message': None,
            'data': None
        }
        self.response = None
        self.code = 200


    def check_json(self):
        self.assertJSONEqual(json.dumps(self.base_json), self.response.content.decode("utf-8"))
        self.assertEqual(self.response.status_code, self.code)
    
    def send_request(self):
        self.response = self.client.post(reverse(update_user),json.dumps(self.content),content_type='application/json')

    def test_valid_update(self):

        self.base_json['status'] = 'success'
        self.base_json['message'] = 'Updated fields'
        self.base_json['data'] = None
        self.content['first_name'] = "Luis"
        self.content['last_name'] = "Soto"
        self.content['tournament_name'] = "Tournament"
        self.send_request()
        self.check_json()

        user = User.objects.get(username=self.user1.username)
        self.assertEqual(user.first_name, "Luis")
        self.assertEqual(user.last_name, "Soto")
        self.assertEqual(user.tournament_name, "Tournament")
        self.check_json()

    def test_invalid_fields(self):
        # updates all valid fields, username can't be updated
        self.base_json['status'] = 'success'
        self.base_json['message'] = 'Updated fields'
        self.base_json['data'] = None

        self.content['first_name'] = "Luis"
        self.content['last_name'] = "Soto"
        self.content['tournament_name'] = "Tournament"
        self.content['username'] = "Different"
        self.send_request()

        user = User.objects.get(username=self.user1.username)
        self.assertEqual(user.first_name, "Luis")
        self.assertEqual(user.last_name, "Soto")
        self.assertEqual(user.tournament_name, "Tournament")
        #username can't be changed
        self.assertEqual(user.username, self.user1.username)
    
        self.check_json()


    def test_empty_data(self):
        self.base_json['status'] = 'error'
        self.base_json['message'] = 'Invalid JSON body'
        self.base_json['data'] = None
        self.code = 400
        self.send_request()
        self.check_json()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
@override_settings(MEDIA_URL='/profile_pictures/', MEDIA_ROOT=os.path.join(BASE_DIR, 'profile_pictures'))
class ProfilePictureRetrievalTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='TestUser', password='testpass')
        self.client = Client()
        self.client.login(username='TestUser', password='testpass')
        self.base_json = {
            'status': None,
            'message': None,
            'data': None
        }
        self.response = None
        self.code = 0

    def check_json(self):
        self.assertJSONEqual(json.dumps(self.base_json), self.response.content.decode("utf-8"))
        self.assertEqual(self.response.status_code, self.code)

    def test_get_default_profile_picture(self):
            self.base_json['status'] = 'success'
            self.base_json['message'] = 'Got profile picture'
            self.base_json['data'] = {
                    'profile_picture_url': '/profile_pictures/default.jpeg'
                    }
            
            self.response = self.client.get(reverse('get_profile_picture', args=['TestUser']))
            self.code = 200
            self.check_json()

@override_settings(MEDIA_URL='/profile_pictures/', MEDIA_ROOT=os.path.join(BASE_DIR, 'profile_pictures'))
class UploadPictureTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='TestUser', password='testpass')
        self.client = Client()
        self.client.login(username='TestUser', password='testpass')
        self.base_json = {
            'status': None,
            'message': None,
            'data': None
        }
        self.response = None
        self.code = 200
        self.test_file_path = os.path.join(settings.MEDIA_ROOT, 'upload_test.png')


    def check_json(self):
        self.assertJSONEqual(json.dumps(self.base_json), self.response.content.decode("utf-8"))
        self.assertEqual(self.response.status_code, self.code)

    def test_upload_picture(self):
        file_path = os.path.join(settings.MEDIA_ROOT, 'upload_test.png')
        with open(file_path, 'rb') as img:
            self.response = self.client.post(
                reverse('upload_picture'),
                {'picture': img},
                format='multipart'  # Django will automatically set the correct Content-Type
            )        
        self.base_json['status'] = 'success'
        self.base_json['message'] = 'Updated profile picture'
        self.base_json['data'] = {'profile_picture_url': '/profile_pictures/TestUser/upload_test.png'}
        self.check_json()        


    def tearDown(self):
        file_path = os.path.join(settings.MEDIA_ROOT, 'TestUser', 'upload_test.png')
        if os.path.isfile(file_path):
            os.remove(file_path)
        
        user_dir = os.path.join(settings.MEDIA_ROOT, 'TestUser')
        if os.path.isdir(user_dir) and not os.listdir(user_dir):
            os.rmdir(user_dir)

class getUserProfile(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(first_name='Luis', last_name='Soto', username='TestUser' ,lowercase_username='testUser', password='testpass', tournament_name='TestUser')
        self.user2 = User.objects.create_user(first_name='Luis', last_name='Soto', username='TestUser2' ,lowercase_username='testUser2', password='testpass', tournament_name='TestUser2')
        self.client = Client()
        self.client.login(username='TestUser', password='testpass')
        self.base_json = {
            'status': None,
            'message': None,
            'data': None
        }
        self.response = None
        self.code = 200


    def check_json(self):
        self.assertJSONEqual(json.dumps(self.base_json), self.response.content.decode("utf-8"))
        self.assertEqual(self.response.status_code, self.code)

    def test_get_self_profile(self):
        self.base_json['status'] = 'success'
        self.base_json['message'] ='Got user profile'
        self.base_json['data'] = {
            'is_online': False,
            'profile_picture_url': '/profile_pictures/default.jpeg',
            'tournament_name': 'TestUser',
            'username': 'TestUser',
            'first_name': 'Luis',
            'last_name': 'Soto',
            }
        self.response = self.client.get(reverse('get_profile',args=[self.user.username]))
        self.check_json()

    def test_get_other_profile(self):
        self.base_json['status'] = 'success'
        self.base_json['message'] ='Got user profile'
        self.base_json['data'] = {
            'is_online': False,
            'profile_picture_url': '/profile_pictures/default.jpeg',
            'tournament_name': 'TestUser2',
            'username': 'TestUser2',
            'first_name': 'Luis',
            'last_name': 'Soto',
            }
        self.response = self.client.get(reverse('get_profile',args=[self.user2.username]))
        self.check_json()

    def test_get_doesnot_exist(self):
        self.base_json['status'] = 'error'
        self.base_json['message'] ='User does not exists'
        self.code = 404
        self.response = self.client.get(reverse('get_profile',args=['i do not exist']))
        self.check_json()

