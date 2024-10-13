from django.shortcuts import render
from django.http import JsonResponse
from web3 import Web3
from blockchainapp.contracts.abi import abi
from blockchainapp.contracts.bytecode import bytecode
from user.models import User
from tournamentsapp.models import Tournaments
from tournamentsapp.wrappers import require_post, user_is_authenticated
import tournaments.settings as settings
# Create your views here.

@require_post
@user_is_authenticated
def execute_contract(request):
	# Conectar a la red (puede ser Ganache o cualquier otro nodo)
	tournament_id = request.data("tournament_id")
	user = User.objects.get(username = request.data("user"))
	if user != tournament.player_id:
		return JsonResponse({'status': 'error', 'message': 'User not authenticated', 'data': None}, status=405)
	tournament = Tournaments.object.get(id = tournament_id)
	try:
		web3 = Web3(Web3.HTTPProvider(settings.GANACHE_URL))
	except:
		return JsonResponse({'status': 'error', 'message': 'Error connecting to the blockchain', 'data': None}, status=500)
	# Leer el contrato
	account = web3.eth.accounts[0]
	contract = web3.eth.contract(address=bytecode, abi=abi)
	first_place = tournament.id_winner.tournament_name
	second_place = tournament.id_second.tournament_name
	third_place = tournament.id_third.tournament_name
	organizer = tournament.player_id.tournament_name
	start_date = tournament.date_start
	transaction = contract.functions.setTournamentResults(first_place,second_place, third_place, organizer,start_date).call()
	# Ejecutar la función del contrato
	contract.functions.setGreeting

	tx = contract.functions.setTournamentResults(first_place, second_place, third_place, start_date).buildTransaction({
				'from': account,
				'nonce': web3.eth.getTransactionCount(account),
				'gas': 2000000,  # Límite de gas
				'gasPrice': web3.toWei('20', 'gwei')  # Precio del gas
			})
	key = tournament.player_id.private_key
	signed_tx = web3.eth.account.signTransaction(tx, private_key=key)
	tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
	reception = web3.eth.waitForTransactionReceipt(tx_hash)
	tournament.hash = tx_hash
	tournament.save()
	return JsonResponse({'status': 'success', 'message': 'Contract executed', 'data': tx_hash}, status=200)

def get_balance_from_web3(wallet):
	print('Red blockchain:', settings.GANACHE_URL)
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

@require_post
@user_is_authenticated
def make_transaction(request):
	user = User.objects.get(username = request.data("user"))
	amount = request.data("amount")
	receiver_id = request.data("receiver")
	receiver = User.objects.get(username = receiver_id)
	try:
		try:
			web3 = Web3(Web3.HTTPProvider(settings.GANACHE_URL))
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
		signed_tx = web3.eth.account.signTransaction(tx, private_key=key)
		tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
		reception = web3.eth.waitForTransactionReceipt(tx_hash)
		return JsonResponse({'status': 'success', 'message': 'Transaction made', 'data': tx_hash}, status=200)
	except:
		return JsonResponse({'status': 'error', 'message': 'Error making transaction', 'data': None}, status=405)