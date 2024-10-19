from tournamentsapp.models import Tournaments, Matches, User
from django.test import TestCase, Client
from django.urls import reverse
from tournamentsapp.views.open_tournament import open_tournament
from tournamentsapp.views.accept_invitation import accept_invitation
from tournamentsapp.views.close_tournament import close_tournament
from tournamentsapp.views.start_match import start_match
from tournamentsapp.views.finish_match import finish_match
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
	print('New account created', user.username,
	      "  wallet  ", user.ethereum_address)
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
		tx, '0x0723b380d3642d13ef2403267c803be6a09eae6f94f7e92f155656a73f251551')
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
			user = User.objects.create_user(
				username=f"test{i}", password="test", tournament_name=f"test{i}")
			transfer_first_founds(user)
