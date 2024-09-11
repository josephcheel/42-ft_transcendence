from tournamentsapp.models import Tournaments, Invitations, Matches, User
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from tournamentsapp.views.views import open_tournament, accept_invitation, close_tournament, start_match, finish_match
from tournamentsapp.views.list_tournaments import list_tournaments
from datetime import timedelta
from django.utils import timezone
from django.db import OperationalError
import json
from tournamentsapp.status_options import StatusTournaments, StatusInvitations, StatusMatches, Rounds
import random
from .printing import print_all_tournaments, print_all_invitations, print_all_matches, print_all_users
from datetime import datetime
# Create your tests here.
#User = get_user_model()

# Create an array of users
class test_open_tournament(TestCase):
	def setUp(self):
		self.client = Client()
		self.users = []
		for i in range(1, 22):
#			request = self.client.post('http://usermanagement:8000/user/create_user/', json.dumps(
#				{'username': f"test{i}", 'password': "test"}), content_type='application/json')
			current_user = User.objects.create(username=f"test{i}", password="test")
		self.base_json = {'status': None, 'message': None, 'data': None}
	
	def check_json(self, response, code):
		self.assertJSONEqual(json.dumps(self.base_json), response.content.decode("utf-8"))
		self.assertEqual(response.status_code, code)

	def test_tournament_creation(self):
		all_users = User.objects.all()
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
		self.base_json['message'] = 'The owner user does not exist'
		self.base_json['data'] = None
		response = self.client.post(
			'/tournaments/open/', json.dumps(self.tournament), content_type='application/json')
		self.check_json(response, 400)

		#Invalid start date
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

		#Max players must be even
		self.tournament = {
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
		response = self.client.post(reverse(open_tournament), json.dumps(self.tournament),content_type='application/json')
		self.check_json(response, 400)

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

class test_accept_invitation (TestCase):
	def setUp(self):
		self.client = Client()
		self.users = []
		for i in range(1, 22):
			current_user = User.objects.create(username=f"test{i}", password="test")

	def check_json(self, response, code):
		self.assertJSONEqual(json.dumps(self.base_json),
		                     response.content.decode("utf-8"))
		self.assertEqual(response.status_code, code)

	def test_accept_invitation(self):
		self.base_json = {'status': None, 'message': None, 'data': None}
		self.tournament = {
			'username': 'test10',
			'password': 'test',
			'date_start': (timezone.now() + timedelta(days=1)).isoformat(),
			'max_players': 14,
			'cost': 10,
			'price_1': 1000,
			'price_2': 500,
			'price_3': 250,
			'players': ['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test15', 'test18', 'test19', 'test20'], }
		self.base_json['status'] = 'success'
		self.base_json['message'] = 'Tournament created successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournament), json.dumps(
			self.tournament), content_type='application/json')
		self.check_json(response, 200)

		# Username is NOK
		self.invitation = {
			'username': 'test122',
			'password': 'test',
			'tournament_id': '1'
		}
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'The user does not exist'
		self.base_json['data'] = None
		response = self.client.post(reverse(accept_invitation), json.dumps(
			self.invitation), content_type='application/json')
		self.check_json(response, 400)

		# Tournament is NOK
		self.invitation = {
			'username': 'test1',
			'password': 'test',
			'tournament_id': '10'
		}
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'The tournament does not exist'
		self.base_json['data'] = None
		response = self.client.post(reverse(accept_invitation), json.dumps(
			self.invitation), content_type='application/json')
		self.check_json(response, 400)

		# Username not invited
		self.invitation = {
			'username': 'test12',
			'password': 'test',
			'tournament_id': '1'
		}
		self.base_json['status'] = 'error'
		self.base_json['message'] = 'You have not been invited to this tournament'
		self.base_json['data'] = None
		response = self.client.post(reverse(accept_invitation), json.dumps(
			self.invitation), content_type='application/json')
		self.check_json(response, 400)
		
		# Username does not have enough points
		self.invitation = {
			'username': 'test7',
			'password': 'test',
			'tournament_id': '1'
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
			'tournament_id': '1'
		}
		self.base_json['status'] = 'success'
		self.base_json['message'] = 'Invitation accepted successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(accept_invitation), json.dumps(
			self.invitation), content_type='application/json')
		self.check_json(response, 200)


class test_close_tournament (TestCase):
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
		self.tournament = {
			'username': 'test10',
			'password': 'test',
			'date_start': (timezone.now() + timedelta(days=1)).isoformat(),
			'max_players': 14,
			'cost': 10,
			'price_1': 1000,
			'price_2': 500,
			'price_3': 250,
			'players': ['test20', 'test19', 'test7', 'test4', 'test13', 'test17', 'test15', 'test16',
                            'test5', 'test6', 'test14', 'test9', 'test11', 'test12'], }
		self.base_json['status'] = 'success'
		self.base_json['message'] = 'Tournament created successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournament), json.dumps(
			self.tournament), content_type='application/json')

		self.check_json(response, 200)
		players = ['test20', 'test19', 'test7', 'test4', 'test13', 'test17', 'test15', 'test16',
                    'test5', 'test6', 'test14', 'test9', 'test11', 'test12']
		for player in players:
			self.invitation = {
				'username': player,
				'password': 'test',
				'tournament_id': '1'
			}
			self.client.post(reverse(accept_invitation), json.dumps(
				self.invitation), content_type='application/json')
			print('player =', player, ' invitacion aceptada',
			      'torneo numero = ', self.invitation['tournament_id'])
		self.invitation = {
			'username': 'test10',
			'password': 'test',
			'tournament_id': '1'
		}
		tournament = Tournaments.objects.get(id = self.invitation['tournament_id'])
		self.base_json['status'] = 'success'
		self.base_json['message'] = 'Tournament closed successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(close_tournament), json.dumps(
			self.invitation), content_type='application/json')
		self.check_json(response, 200)

		# Everithing is OK with 4 players
		self.tournament = {
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
		self.base_json['message'] = 'Tournament created successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournament), json.dumps(
			self.tournament), content_type='application/json')
		self.check_json(response, 200)
		players = ['test9', 'test10', 'test11', 'test12']
		for player in players:
			self.invitation = {
				'username': player,
                'password': 'test',
				'tournament_id': '2'
			}
			print('player =', player, ' invitacion aceptada', 'torneo numero = ', self.invitation['tournament_id'])
			self.base_json['status'] = 'success'
			self.base_json['message'] = 'Invitation accepted successfully'
			self.base_json['data'] = None
			response = self.client.post(reverse(accept_invitation), json.dumps(
				self.invitation), content_type='application/json')
			self.check_json(response, 200)

		self.close = {
			'username': 'test10',
			'password': 'test',
			'tournament_id': '2'
		}
		tournament = Tournaments.objects.get(id=self.invitation['tournament_id'])
		self.base_json['status'] = 'success'
		self.base_json['message'] = 'Tournament closed successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(close_tournament), json.dumps(
			self.close), content_type='application/json')
		self.check_json(response, 200)

		# Everithing is OK with 2 players
		self.tournament = {
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
		self.base_json['message'] = 'Tournament created successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournament), json.dumps(
			self.tournament), content_type='application/json')
		self.check_json(response, 200)
		players = ['test9', 'test10']
		for player in players:
			self.invitation = {
				'username': player,
				'password': 'test',
				'tournament_id': '3'
			}
			print('player =', player, ' invitacion aceptada', 'torneo numero = ', self.invitation['tournament_id'])
			self.base_json['status'] = 'success'
			self.base_json['message'] = 'Invitation accepted successfully'
			self.base_json['data'] = None
			response = self.client.post(reverse(accept_invitation), json.dumps(
				self.invitation), content_type='application/json')
			self.check_json(response, 200)

		self.close = {
			'username': 'test10',
			'password': 'test',
			'tournament_id': '3'
		}
		self.base_json['status'] = 'success'
		self.base_json['message'] = 'Tournament closed successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(close_tournament), json.dumps(
			self.close), content_type='application/json')
		self.check_json(response, 200)

		# play matches and finish tournament
		while tournament.status != StatusTournaments.FINISHED_TOURNAMENT.value:
			matches = Matches.objects.filter(
				tournament_id=1, status=StatusMatches.NOT_PLAYED.value, number_round=tournament.current_round)
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
			tournament = Tournaments.objects.get(id=1)
		print_all_tournaments()
		print_all_invitations()
		print_all_matches()
		print_all_users()

class test_list_tournaments(TestCase):

	def setUp(self):
		self.client = Client()
		self.users = []
		for i in range(1, 22):
			current_user = User.objects.create(username=f"test{i}", password="test")
		self.base_json = {'status': None, 'message': None, 'data': None}
	
	def check_json(self, response, code):
		self.assertJSONEqual(json.dumps(self.base_json), response.content.decode("utf-8"))
		self.assertEqual(response.status_code, code)

	def test_list_tournaments(self):
		self.tournament = {
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
		self.base_json['message'] = 'Tournament created successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournament), json.dumps(
			self.tournament), content_type='application/json')
		self.check_json(response, 200)
		self.tournament = {
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
		self.base_json['message'] = 'Tournament created successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournament), json.dumps(
			self.tournament), content_type='application/json')
		self.check_json(response, 200)

		self.tournament = {
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
		self.base_json['message'] = 'Tournament created successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournament), json.dumps(
			self.tournament), content_type='application/json')
		self.check_json(response, 200)

		self.list_tournaments = {
			'username': 'test10',
			'password': 'test'}
		owner = User.objects.get(username='test10')
		tournament_data = Tournaments.objects.filter(player_id=owner.id)

		# Convert any datetime fields to string
		tournament_list = list(tournament_data.values())
		for tournament in tournament_list:
			for key, value in tournament.items():
				if isinstance(value, datetime):
					tournament[key] = value.isoformat()
		self.base_json['status'] = 'success'
		self.base_json['message'] = 'List of tournaments cereated'
		self.base_json['data'] = json.dumps(tournament_list)
		print (self.base_json['data'])
		url = reverse(list_tournaments)
		print (url)
		response = self.client.get(reverse(list_tournaments), json.dumps(
			self.list_tournaments), content_type='application/json')
		print(response.content.decode("utf-8"))	
		self.check_json(response, 200)
