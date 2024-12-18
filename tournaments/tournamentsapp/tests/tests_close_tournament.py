from tournamentsapp.models import Tournaments, Matches, User
from django.test import TestCase, Client
from django.urls import reverse
from tournamentsapp.views.open_tournament import open_tournament
from tournamentsapp.views.accept_invitation import accept_invitation
from tournamentsapp.views.close_tournament import close_tournament
from tournamentsapp.views.start_match import start_match
from tournamentsapp.views.finish_match import finish_match
from tournamentsapp.views.list_matches import list_matches
from django.db.models import Q

from datetime import timedelta
from django.utils import timezone
import json
import requests
from tournamentsapp.status_options import StatusTournaments, StatusMatches
import random
from .printing import print_all_tournaments, print_all_invitations, print_all_matches, print_all_users
from tournamentsapp.tasks.check_match_db_status import check_match_db_status
from web3 import Web3
from django.conf import settings

# Create your tests here.

def transfer_first_founds(user):
	web3 = Web3(Web3.HTTPProvider(settings.GANACHE_URL))
	ganache_url = settings.GANACHE_URL
	web3 = Web3(Web3.HTTPProvider(ganache_url))
	if not web3.is_connected():
		print("Could not connect to blockchain")
		return False
	print("Connected to blockchain")
	new_account = web3.eth.account.create()
	user.ethereum_address = new_account.address
	user.ethereum_private_key = '0x' + new_account._private_key.hex()
	user.save()
	print('New account created', user.username, "  wallet  ", user.ethereum_address)
	print('private key', user.ethereum_private_key)
	print('Transfering 10 ethers to ', user.ethereum_address)
	print('Transfering 10 ethers from ', web3.eth.accounts[0])
	ganache_bank_account = web3.eth.accounts[0]
	tx = {'from': ganache_bank_account,
		  'to': user.ethereum_address,
		  'value': web3.to_wei(10, 'ether'),
		  'gas': 21000,
		  'gasPrice': Web3.to_wei('1', 'gwei'),
		  'nonce': web3.eth.get_transaction_count(ganache_bank_account)}
	signed_tx = web3.eth.account.sign_transaction(
		tx, settings.GANACHE_BANK)
	tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
	web3.eth.wait_for_transaction_receipt(tx_hash)
	print('Balance after transfer', web3.eth.get_balance(user.ethereum_address))
	return True


class test_close_tournament (TestCase):
	def setUp(self):
		self.client = Client()
		self.base_json = {'status': None, 'message': None, 'data': None}

	def check_json(self, response, code):
		self.assertJSONEqual(json.dumps(self.base_json),
							 response.content.decode("utf-8"))
		self.assertEqual(response.status_code, code)

	def test_complete_process(self):
		self.cookies = {}
		is_json_header = {'Content-Type': 'application/json'}
		for i in range(1, 22):
			print('Creating user test', i)
			user = User.objects.create_user(username=f"test{i}", password="test", tournament_name=f"test{i}")
			transfer_first_founds(user)
		# Everithing is OK with 12 players
		self.client.login(username='test10', password='test')
		self.tournament = {
			'username': 'test10',
			'password': 'test',
			'name': 'test10_tournament',
			'date_start': (timezone.now() + timedelta(days=1)).isoformat(),
			'max_players': 14,
			'cost': 10,
			'price_1': 1000,
			'price_2': 500,
			'price_3': 250,
			'winnig_points': 5,
			'players': ['test20', 'test19', 'test7', 'test4', 'test13', 'test17', 'test15', 'test16',
						'test5', 'test6', 'test14', 'test9', 'test11', 'test12'], }
		self.base_json['status'] = 'success'
		self.base_json['message'] = 'Tournament created successfully'
		self.base_json['data'] = None
		response = self.client.post(reverse(open_tournament), json.dumps(
			self.tournament), content_type='application/json')
		self.check_json(response, 200)
		self.client.logout()
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
			'name': 'test10_tournament2',
			'date_start': (timezone.now() + timedelta(days=1)).isoformat(),
			'max_players': 14,
			'cost': 10,
			'price_1': 1000,
			'price_2': 500,
			'price_3': 250,
			'winning_points': 5,	
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
			'name': 'test10_tournament3',
			'date_start': (timezone.now() + timedelta(days=1)).isoformat(),
			'max_players': 14,
			'cost': 10,
			'price_1': 1000,
			'price_2': 500,
			'price_3': 250,
			'winning_points': 6,
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
				points_looser = random.randint(0, 5)
				self.match_to_finish = {'match_id': match.id,'winner': the_winner_id, 'looser': the_looser_id, 'points_winner': tournament.winning_points, 'points_looser': points_looser}
				self.base_json['status'] = 'success'
				self.base_json['message'] = 'Match finished successfully'
				self.base_json['data'] = None
				response = self.client.post(reverse(finish_match), json.dumps(
					self.match_to_finish), content_type='application/json')
				self.check_json(response, 200)
				print('match =', match.id, ' finished. Won!!!!', the_winner_id, ' lost ', the_looser_id)
				check_match_db_status.delay()
			tournament = Tournaments.objects.get(id=1)
		print_all_tournaments()
		print_all_invitations()
		print_all_matches()
		print_all_users()
	def test_list_matches(self):
		self.client.login(username='test10', password='test')
		test10User = User.objects.get(username='test10')
		matches = {
			'username': 'test10',
		}
		self.base_json['status'] = 'success'
		self.base_json['message'] = 'List of matches'
		list_of_matches = Matches.objects.filter(Q(player_id_1=test10User) | Q(player_id_2__username=test10User))
		json.dumps()
		self.base_json['data'] = json.dumps(list_of_matches)
		response = self.client.post(reverse(list_matches), json.dumps(
			matches), content_type='application/json')
		print (response.content)
		self.check_json(response, 200)
		self.client.logout()
