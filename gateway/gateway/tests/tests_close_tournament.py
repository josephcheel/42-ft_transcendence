from django.test import TestCase, Client
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone
import json
import requests
import random
# Create your tests here.
from django.contrib.auth import get_user_model
User = get_user_model()

class test_close_tournament (TestCase):
	def setUp(self):
		self.base_json = {'status': None, 'message': None, 'data': None}
		self.create_user_url = 'http://usermanagement:8000/user/create_user/'
		self.login_user_url = 'http://usermanagement:8000/user/login_user/'
		self.logout_user_url = 'http://usermanagement:8000/user/logout_user/'
		self.is_logged_in_url = 'http://usermanagement:8000/user/is_logged_in/'
		self.open_tournament_url = 'http://tournaments:8000/tournaments/open_tournament/'
	def check_json(self, response, code):
		self.assertJSONEqual(json.dumps(self.base_json),
		                     response.content.decode("utf-8"))
		self.assertEqual(response.status_code, code)

	def test_complete_process(self):
		self.mysessions = {}
		is_json_header = {'Content-Type': 'application/json'}
		for i in range(1, 22):
			print('Creating user test', i)
			headers = {
				'Content-Type': 'application/json',
			}
			my_data = json.dumps({'username': f"test{i}", 'password': "test", 'first_name': f"test{i}", 'last_name': f"Apellido{i}"})
			self.mysessions[f'test{i}'] = requests.Session()
			my_response = self.mysessions[f'test{i}'].post(self.create_user_url, data=my_data, headers=headers)
			print(my_response.content)
			my_data = json.dumps({'username': f"test{i}", 'password': "test"})
			my_response = self.mysessions[f'test{i}'].post(self.login_user_url, data=my_data, headers=headers)
			print(my_response.content)
			self.mysessions[f'test{i}'].get(self.is_logged_in_url)
			print(my_response.content)
#			User.objects.create_user(username=f"test{i}", password="test")
		# Everithing is OK with 12 players
#		self.client.logout()
#		self.client.login(username='test10', password='test')
		headers = {
			'Content-Type': 'application/json',
		}
		my_data = {
			'username': 'test4',
			'password': 'test',
			'date_start': (timezone.now() + timedelta(days=1)).isoformat(),
			'max_players': 14,
			'cost': 10,
			'price_1': 1000,
			'price_2': 500,
			'price_3': 250,
			'players': ['test20', 'test19', 'test7', 'test4', 'test13', 'test17', 'test15', 'test16',
						'test5', 'test6', 'test14', 'test9', 'test11', 'test12'], }
		my_response = self.mysessions['test4'].post(self.open_tournament_url, data=json.dumps(my_data), headers=headers)
		print('Answer from open_tournament?', my_response.content)
		self.base_json['status'] = 'success'
		self.base_json['message'] = 'Tournament created successfully'
		self.base_json['data'] = None
#		response = self.client.post(reverse(open_tournament), json.dumps(self.tournament), content_type='application/json')
		self.check_json(my_response, 200)
		input('Press enter to continue')
		players = ['test20', 'test19', 'test7', 'test4', 'test13', 'test17', 'test15', 'test16',
                    'test5', 'test6', 'test14', 'test9', 'test11', 'test12']
		for player in players:
			self.client.login(username=player, password='test')
			self.invitation = {
				'tournament_id': '1'
			}
			self.client.post(reverse(accept_invitation), json.dumps(
				self.invitation), content_type='application/json')
			self.client.logout()

		self.client.login(username='test10', password='test')
		self.invitation = {
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
		my_data = json.dumps({'username': "test10", 'password': "test"})
		self.client.logout()
		self.client.login(username='test10', password='test')
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
		
		self.client.logout()
		players = ['test9', 'test10', 'test11', 'test12']
		for player in players:
			self.client.login(username=player, password='test')
			self.invitation = {
				'tournament_id': '2'
			}
			self.base_json['status'] = 'success'
			self.base_json['message'] = 'Invitation accepted successfully'
			self.base_json['data'] = None
			response = self.client.post(reverse(accept_invitation), json.dumps(
				self.invitation), content_type='application/json')
			self.check_json(response, 200)
			self.client.logout()
			
		self.client.login(username='test10', password='test')	
		self.close = {
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
		
		self.client.logout()
		for player in players:
			self.client.login(username=player, password='test')
			self.invitation = {
				'tournament_id': '3'
			}
			self.base_json['status'] = 'success'
			self.base_json['message'] = 'Invitation accepted successfully'
			self.base_json['data'] = None
			response = self.client.post(reverse(accept_invitation), json.dumps(
				self.invitation), content_type='application/json')
			self.check_json(response, 200)
			self.client.logout()

		self.client.login(username='test10', password='test')
		self.close = {
			'tournament_id': '3'
		}
		self.base_json['status'] = 'success'
		self.base_json['message'] = 'Tournament closed successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(close_tournament), json.dumps(
			self.close), content_type='application/json')
		self.check_json(response, 200)
		self.client.logout()

		# play matches and finish tournament
		print('======================== Play matches and finish tournament========================')
		while tournament.status != StatusTournaments.FINISHED_TOURNAMENT.value:
			matches = Matches.objects.filter(
				tournament_id=1, status=StatusMatches.NOT_PLAYED.value, number_round=tournament.current_round)
			for match in matches:
				if random.choice([True, False]):
					self.client.login(username=match.player_id_1.username, password='test')
					self.match_to_play = {'match_id': match.id}
					self.base_json['status'] = 'success'
					self.base_json['message'] = 'Waiting for player 2 to start the match'
					self.base_json['data'] = json.dumps({'status': 'waiting player 2'})
					response = self.client.post(reverse(start_match), json.dumps(self.match_to_play), content_type='application/json')
					self.check_json(response, 200)
					self.client.logout()
					self.client.login(username=match.player_id_2.username, password='test')
					self.match_to_play = {'match_id': match.id}
					self.base_json['status'] = 'success'
					self.base_json['message'] = 'Match started successfully'
					self.base_json['data'] = json.dumps({'status': 'started'})
					response = self.client.post(reverse(start_match), json.dumps(self.match_to_play), content_type='application/json')
					self.check_json(response, 200)
					self.client.logout()
				else:
					self.client.login(username=match.player_id_2.username, password='test')
					self.match_to_play = {'match_id': match.id}
					self.base_json['status'] = 'success'
					self.base_json['message'] = 'Waiting for player 1 to start the match'
					self.base_json['data'] = json.dumps({'status': 'waiting player 1'})
					response = self.client.post(reverse(start_match), json.dumps(self.match_to_play), content_type='application/json')
					self.check_json(response, 200)
					self.client.logout()
					self.client.login(username=match.player_id_1.username, password='test')
					self.match_to_play = {'match_id': match.id}
					self.base_json['status'] = 'success'
					self.base_json['message'] = 'Match started successfully'
					self.base_json['data'] = json.dumps({'status': 'started'})
					response = self.client.post(reverse(start_match), json.dumps(self.match_to_play), content_type='application/json')
					self.check_json(response, 200)
					self.client.logout()

				print('match =', match.id, ' started!!!! player', match.player_id_1.username, ' vs ', match.player_id_2.username, ' round = ', match.round, ' number_round = ', match.number_round)
				if random.choice([True, False]):
					the_winner_id = match.player_id_2.username
					the_looser_id = match.player_id_1.username
				else:
					the_winner_id = match.player_id_1.username
					the_looser_id = match.player_id_2.username
				self.match_to_finish = {'match_id': match.id,'winner': the_winner_id, 'looser': the_looser_id}
				self.base_json['status'] = 'success'
				self.base_json['message'] = 'Match finished successfully'
				self.base_json['data'] = None
				response = self.client.post(reverse(finish_match), json.dumps(
					self.match_to_finish), content_type='application/json')
				self.check_json(response, 200)
				print('match =', match.id, ' finished. Won!!!!', the_winner_id, ' lost ', the_looser_id)
				input('Press enter to continue')
				check_match_db_status.delay()
			tournament = Tournaments.objects.get(id=1)
		print_all_tournaments()
		print_all_invitations()
		print_all_matches()
		print_all_users()
