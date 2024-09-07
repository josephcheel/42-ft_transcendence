from tournementsapp.models import Tournements, Invitations, Matches, User
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from tournementsapp.views import open_tournement, accept_invitation, close_tournement, start_match, finish_match
from datetime import timedelta
from django.utils import timezone
from django.db import OperationalError
import json
from tournementsapp.status_options import StatusTournements, StatusInvitations, StatusMatches, Rounds
import random
from .printing import print_all_tournements, print_all_invitations, print_all_matches, print_all_users
# Create your tests here.
#User = get_user_model()

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

	def test_tournement_creation(self):
		for i in range(1, 22):
			User.objects.create(username=f"test{i}", password="test")
		all_users = User.objects.all()
		self.tournement = Client()

		#Owner does not exist
		self.tournement = {
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
		self.base_json['message'] = 'The owner user does not exist'
		self.base_json['data'] = None
		response = self.client.post(
			'/tournements/open/', json.dumps(self.tournement), content_type='application/json')
		self.check_json(response, 400)

		#Invalid start date
		self.tournement = {
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
		response = self.client.post(reverse(open_tournement), json.dumps(self.tournement), content_type='application/json')
		self.check_json(response, 400)

		#Max players must be even
		self.tournement = {
			'username': 'test10', 
			'password': 'test',
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
		response = self.client.post(reverse(open_tournement), json.dumps(self.tournement),content_type='application/json')
		self.check_json(response, 400)

		#Cost or cost must be positive
		self.tournement = {
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
		response = self.client.post(reverse(open_tournement), json.dumps(self.tournement), content_type='application/json')
		self.check_json(response, 400)

		# Prices or cost must be positive
		self.tournement = {
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
		response = self.client.post(reverse(open_tournement), json.dumps(self.tournement), content_type='application/json')
		self.check_json(response, 400)

		# Prices or cost must be positive
		self.tournement = {
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
		response = self.client.post(reverse(open_tournement), json.dumps(self.tournement), content_type='application/json')
		self.check_json(response, 400)

		# Prices or cost must be positive
		self.tournement = {
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
		response = self.client.post(reverse(open_tournement), json.dumps(self.tournement), content_type='application/json')
		self.check_json(response, 400)

		# All players invited must exist
		self.tournement = {
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
		response = self.client.post(reverse(open_tournement), json.dumps(
			self.tournement), content_type='application/json')
		self.check_json(response, 400)

		# Everithing is ok
		self.tournement = {
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
		self.base_json['message'] = 'Tournement created successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournement), json.dumps(
			self.tournement), content_type='application/json')
		self.check_json(response, 200)

class test_accept_invitation (TestCase):
	def setUp(self):
		self.client = Client()
		self.users = []
		for i in range(1, 22):
			current_user = User.objects.create(username=f"test{i}", password="test")
		self.base_json = {'status': None, 'message': None, 'data': None}
		player_owner = User.objects.get(username='test1')
		tournement_created = Tournements.objects.create(
			player_id=player_owner.id,
			date_start=(timezone.now() + timedelta(days=1)).isoformat(),
			last_match_date=(timezone.now() + timedelta(days=1)).isoformat(),
			date_max_end=timezone.now()+ timedelta(minutes= 20 * 5 + 30),
			max_players=12,
			cost=10,
			current_round=3,
			price_1=1000,
			price_2=2000,
			price_3=3000,
			id_winner=0,
			id_second=0,
			id_third=0,
			status=StatusTournements.OPEN_TOURNEMENT.value)
		players = ['test1', 'test2', 'test3', 'test4',
                    'test5', 'test6', 'test7', 'test8', 'test9', 'test10']
		for player in players:
			player_reg = User.objects.get(username=player)
			Invitations.objects.create(tournement_id=tournement_created.id,
									player_id=player_reg.id, status=StatusInvitations.INVITATION_IGNORED.value)

	def check_json(self, response, code):
		self.assertJSONEqual(json.dumps(self.base_json),
		                     response.content.decode("utf-8"))
		self.assertEqual(response.status_code, code)

	def test_accept_invitation(self):
		# Username is NOK
		self.invitation = {
			'username': 'test122',
			'password': 'test',
			'tournement_id': '1'
		}
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'The user does not exist'
		self.base_json['data'] = None
		response = self.client.post(reverse(accept_invitation), json.dumps(
			self.invitation), content_type='application/json')
		self.check_json(response, 400)

		# Tournement is NOK
		self.invitation = {
			'username': 'test1',
			'password': 'test',
			'tournement_id': '10'
		}
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'The tournement does not exist'
		self.base_json['data'] = None
		response = self.client.post(reverse(accept_invitation), json.dumps(
			self.invitation), content_type='application/json')
		self.check_json(response, 400)

		# Username not invited
		self.invitation = {
			'username': 'test12',
			'password': 'test',
			'tournement_id': '1'
		}
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'You have not been invited to this tournement'
		self.base_json['data'] = None
		response = self.client.post(reverse(accept_invitation), json.dumps(
			self.invitation), content_type='application/json')
		self.check_json(response, 400)
		
		# Username does not have enough points
		self.invitation = {
			'username': 'test7',
			'password': 'test',
			'tournement_id': '1'
		}
		current_user = User.objects.get(username = self.invitation['username'])
		current_user.puntos = 0
		current_user.save()
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'You do not have enough points to accept the invitation'
		self.base_json['data'] = None
		response = self.client.post(reverse(accept_invitation), json.dumps(
			self.invitation), content_type='application/json')
		self.check_json(response, 400)

	# Accept invitation is ok
		self.invitation = {
			'username': 'test2',
			'password': 'test',
			'tournement_id': '1'
		}
		self.base_json['status'] = 'success'
		self.base_json['message'] = 'Invitation accepted successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(accept_invitation), json.dumps(
			self.invitation), content_type='application/json')
		self.check_json(response, 200)


class test_close_tournement (TestCase):
	def setUp(self):
		self.client = Client()
		self.users = []
		for i in range(1, 22):
			current_user = User.objects.create(username=f"test{i}", password="test")
		self.base_json = {'status': None, 'message': None, 'data': None}

	def check_json(self, response, code):
		self.assertJSONEqual(json.dumps(self.base_json),
		                     response.content.decode("utf-8"))
		self.assertEqual(response.status_code, code)

	def test_complete_process(self):
		
		# Everithing is OK with 12 players
		self.tournement = {
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
		self.base_json['message'] = 'Tournement created successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournement), json.dumps(
			self.tournement), content_type='application/json')

		self.check_json(response, 200)
		players = ['test20', 'test19', 'test7', 'test4',
                    'test5', 'test6', 'test14', 'test9', 'test11']
		for player in players:
			self.invitation = {
				'username': player,
				'password': 'test',
				'tournement_id': '1'
			}
			self.client.post(reverse(accept_invitation), json.dumps(
				self.invitation), content_type='application/json')
		self.invitation = {
			'username': 'test10',
			'password': 'test',
			'tournement_id': '1'
		}
		tournement = Tournements.objects.get(id = self.invitation['tournement_id'])
		self.base_json['status'] = 'success'
		self.base_json['message'] = 'Tournement closed successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(close_tournement), json.dumps(
			self.invitation), content_type='application/json')
		self.check_json(response, 200)

		# Everithing is OK with 4 players
		self.tournement = {
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
		self.base_json['message'] = 'Tournement created successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournement), json.dumps(
			self.tournement), content_type='application/json')
		self.check_json(response, 200)
		players = ['test9', 'test10', 'test11', 'test12']
		for player in players:
			print ('player =', player , ' invitacion aceptada')
			self.invitation = {
				'username': player,
                'password': 'test',
				'tournement_id': '2'
			}
			self.base_json['status'] = 'success'
			self.base_json['message'] = 'Invitation accepted successfully'
			self.base_json['data'] = None
			response = self.client.post(reverse(accept_invitation), json.dumps(
				self.invitation), content_type='application/json')
			self.check_json(response, 200)

		self.close = {
			'username': 'test10',
			'password': 'test',
			'tournement_id': '2'
		}
		tournement = Tournements.objects.get(id=self.invitation['tournement_id'])
		self.base_json['status'] = 'success'
		self.base_json['message'] = 'Tournement closed successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(close_tournement), json.dumps(
			self.close), content_type='application/json')
		self.check_json(response, 200)

		# Everithing is OK with 2 players
		self.tournement = {
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
		self.base_json['message'] = 'Tournement created successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournement), json.dumps(
			self.tournement), content_type='application/json')
		self.check_json(response, 200)
		players = ['test9', 'test10']
		for player in players:
			print('player =', player, ' invitacion aceptada')
			self.invitation = {
				'username': player,
				'password': 'test',
				'tournement_id': '3'
			}
			self.base_json['status'] = 'success'
			self.base_json['message'] = 'Invitation accepted successfully'
			self.base_json['data'] = None
			response = self.client.post(reverse(accept_invitation), json.dumps(
				self.invitation), content_type='application/json')
			self.check_json(response, 200)

		self.close = {
			'username': 'test10',
			'password': 'test',
			'tournement_id': '3'
		}
		self.base_json['status'] = 'success'
		self.base_json['message'] = 'Tournement closed successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(close_tournement), json.dumps(
			self.close), content_type='application/json')
		self.check_json(response, 200)

		# play matches and finish tournement
		while tournement.status != StatusTournements.FINISHED_TOURNEMENT.value:
			matches = Matches.objects.filter(
				tournement_id=1, status=StatusMatches.NOT_PLAYED.value, number_round=tournement.current_round)
			for match in matches:
				player_1 = User.objects.get(id=match.player_id_1)
				player_2 = User.objects.get(id=match.player_id_2)
				print('match =', match.match_id, ' started', player_1.username, ' vs ', player_2.username, ' round = ', match.round, ' number_round = ', match.number_round)
				self.match_to_play = {'match_id': match.match_id, 'player': player_1.username}
				self.base_json['status'] = 'success'
				self.base_json['message'] = 'Match started successfully'
				self.base_json['data'] = None
				response = self.client.post(reverse(start_match), json.dumps(
					self.match_to_play), content_type='application/json')
				self.check_json(response, 200)
				if random.choice([True, False]):
					the_winner_id = player_1.username
					the_looser_id = player_2.username
				else:
					the_winner_id = player_2.username
					the_looser_id = player_1.username
				print('match =', match.match_id, ' finished. Won', the_winner_id, ' lost ', the_looser_id)
				self.match_to_finish = {'match_id': match.match_id,
	                           'winner': the_winner_id, 'looser': the_looser_id}
				self.base_json['status'] = 'success'
				self.base_json['message'] = 'Match finished successfully'
				self.base_json['data'] = None
				response = self.client.post(reverse(finish_match), json.dumps(
					self.match_to_finish), content_type='application/json')
				self.check_json(response, 200)
			tournement = Tournements.objects.get(id=1)
		print_all_tournements()
		print_all_invitations()
		print_all_matches()
		print_all_users()