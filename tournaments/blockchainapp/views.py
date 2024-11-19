from django.shortcuts import render
from django.http import JsonResponse
from web3 import Web3
from blockchainapp.contracts.abi import abi
from blockchainapp.contracts.bytecode import bytecode
from user.models import User
from tournamentsapp.models import Tournaments
from tournamentsapp.wrappers import require_post, user_is_authenticated, validate_json
import tournaments.settings as settings
import time
import logging
import json

logger = logging.getLogger('django')
# Create your views here.

def execute_contract(tournament_id):
	# Conectar a la red (puede ser Ganache o cualquier otro nodo)
	tournament = Tournaments.objects.get(id=tournament_id)
	user = tournament.player_id
	try:
		web3 = Web3(Web3.HTTPProvider(settings.GANACHE_URL))
	except:
		return JsonResponse({'status': 'error', 'message': 'Error connecting to the blockchain', 'data': None}, status=500)
	# Leer el contrato
	account =user.ethereum_address
	contract = web3.eth.contract(address=account, abi=abi)
	first_place = "Nobody" if tournament.id_winner == None else tournament.id_winner.tournament_name
	second_place = "Nobody" if tournament.id_second == None else tournament.id_second.tournament_name
	third_place = "Nobody" if tournament.id_third == None else tournament.id_third.tournament_name
	organizer = tournament.player_id.tournament_name
	start_date = tournament.date_start
	print ('arguments: ', first_place, second_place, third_place, organizer, start_date)
	transaction = contract.functions.setTournamentResults(
		first_place, second_place, third_place, organizer, int(time.mktime(start_date.timetuple()))).call()
	# Ejecutar la función del contrato
#	contract.functions.setGreeting
	tx = contract.functions.setTournamentResults(first_place, second_place, third_place, organizer, int(time.mktime(start_date.timetuple()))).build_transaction({
				'from': account,
				'nonce': web3.eth.get_transaction_count(account),
				'gas': 2000000,  # Límite de gas
				'gasPrice': web3.to_wei('20', 'gwei')  # Precio del gas
			})
	key = user.ethereum_private_key
	signed_tx = web3.eth.account.sign_transaction(tx, private_key=key)
	tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
	web3.eth.wait_for_transaction_receipt(tx_hash)
	tournament.hash = tx_hash
	tournament.save()
    #return JsonResponse({'status': 'success', 'message': 'Contract executed', 'data': tx_hash}, status=200)

def get_balance_from_web3(wallet):
	try:
		web3 = Web3(Web3.HTTPProvider(settings.GANACHE_URL))
	except:
		raise Exception('Error connecting to the blockchain')
	balance = web3.eth.get_balance(wallet)
	return balance

@require_post
@user_is_authenticated
def get_balance(request):
	user = User.objects.get(username = request.data("user"))
	try:
		account = user.ethereum_address
		balance = get_balance_from_web3(account)
		return JsonResponse({'status': 'success', 'message': 'Balance obtained', 'data': balance}, status=200)
	except:
		return JsonResponse({'status': 'error', 'message': 'Error obtaining balance', 'data': None}, status=500)

def make_transaction(request):
	user = User.objects.get(username = request.data("user"))
	amount = request.data("amount")
	receiver_id = request.data("receiver")
	receiver = User.objects.get(username = receiver_id)
	try:
		try:
			web3 = Web3(Web3.HTTPProvider(settings.GANACHE_URL))
			logger.info('Connected to the blockchain')
		except:
			return JsonResponse({'status': 'error', 'message': 'Error connecting to the blockchain', 'data': None}, status=500)
		account = user.ethereum_address
		key = user.ethereum_private_key
		tx = {
			'nonce': web3.eth.getTransactionCount(account),
			'to': receiver.ethereum_address,
			'value': web3.toWei(amount, 'ether'),
			'gas': 2000000,
			'gasPrice': web3.toWei('20', 'gwei')
		}
		signed_tx = web3.eth.account.sign_transaction(tx, private_key=key)
		tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
		web3.eth.wait_for_transaction_receipt(tx_hash)
		return JsonResponse({'status': 'success', 'message': 'Transaction made', 'data': tx_hash}, status=200)
	except:
		return JsonResponse({'status': 'error', 'message': 'Error making transaction', 'data': None}, status=405)

@require_post
@user_is_authenticated
@validate_json
def get_results_from_blockchain(request):
	data = request.data	
	tournament_id = data.get("tournament_id")
	try:
		tournament = Tournaments.objects.get(id=tournament_id)
		try:
			web3 = Web3(Web3.HTTPProvider(settings.GANACHE_URL))
			logger.info('Connected to the blockchain')
		except:
			return JsonResponse({'status': 'error', 'message': 'Error connecting to the blockchain', 'data': None}, status=500)
		contract_addr = tournament.hash

		# ABI del contrato (exportada al compilar el contrato en Remix/Hardhat/Truffle)
		abi = [
			{
				"inputs": [],
				"name": "getTournamentResults",
				"outputs": [
					{"internalType": "string", "name": "firstPlace", "type": "string"},
					{"internalType": "string", "name": "secondPlace", "type": "string"},
					{"internalType": "string", "name": "thirdPlace", "type": "string"},
					{"internalType": "string", "name": "organizer", "type": "string"},
					{"internalType": "uint256", "name": "startDate", "type": "uint256"},
					{"internalType": "address", "name": "owner", "type": "address"},
				],
				"stateMutability": "view",
				"type": "function",
			}
		]
		contract = web3.eth.contract(address=contract_addr, abi=abi)
		results = contract.functions.getTournamentResults().call()
		my_data = json.dumps({
			'first_place': results[0],
			'second_place': results[1],
			'third_place': results[2],
			'organizer': results[3],
			'start_date': results[4]
		})
		return JsonResponse({'status': 'success', 'message': 'Results obtained', 'data': my_data}, status=200)
	except:
		return JsonResponse({'status': 'error', 'message': 'Error obtaining results', 'data': None}, status=500)