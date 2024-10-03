from django.shortcuts import render
from django.http import JsonResponse
from web3 import Web3
from blockchainapp.contracts.abi import abi
from blockchainapp.contracts.bytecode import bytecode
from users.models import User
from tournamentsapp.models import Tournaments
from tournamentsapp.wrappers import require_post, user_is_authenticated
# Create your views here.

def connection(request):
	# Conectar a la red (puede ser Ganache o cualquier otro nodo)
	print(request)
	ganache_url = "http://blockchain:8545"
	web3 = Web3(Web3.HTTPProvider(ganache_url))
	print ("paso")
	# Verificar conexión
	if web3.is_connected():
		print("Conectado a la blockchain")
		return render(request, 'connection.html', {'status': 'Conectado a la blockchain'})
	else:
		print("Error de conexión")
		return render(request, 'connection.html', {'status': 'Error de conexión'})

@require_post
@user_is_authenticated
def execute_contract(request):
	# Conectar a la red (puede ser Ganache o cualquier otro nodo)
	tournament_id = request.data("tournament_id")
	user = User.objects.get(username = request.data("user"))
	if user != tournament.player_id:
		return JsonResponse({'status': 'error', 'message': 'User not authenticated', 'data': None}, status=405)
	tournament = Tournaments.object.get(id = tournament_id)
	ganache_url = "http://blockchain:8545"
	web3 = Web3(Web3.HTTPProvider(ganache_url))
	# Verificar conexión
	if web3.is_connected():
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
