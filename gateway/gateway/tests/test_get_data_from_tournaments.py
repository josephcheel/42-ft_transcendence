from web3 import Web3
from abi import abi
from bytecode import bytecode
import json
import pytz
import time
from datetime import datetime

EuropeZone = pytz.timezone('Europe/Madrid')
DOMAIN = 'http://10.11.249.237:8545/'
bank_private_key = "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"

def connect_to_blockchain():
	try:
		web3 = Web3(Web3.HTTPProvider(DOMAIN))
		print('Connected to the blockchain')
	except:
		print ('Error connecting to the blockchain')
	return web3

def create_account(web3:Web3):
	new_account = web3.eth.account.create()
	address_account = new_account.address
	private_key =  '0x' + new_account._private_key.hex()
	print ("my_Wallet = ", address_account)
	print ("my private_key = ", private_key )
	ganache_bank_account = web3.eth.accounts[0]
	print("bank account: ",ganache_bank_account)
	print("balance Bakn: ",web3.eth.get_balance(ganache_bank_account))
	tx = {'from': ganache_bank_account,
        'to': address_account,
		'value': web3.to_wei(100, 'ether'),
		'gas': 21000,
		'gasPrice': Web3.to_wei('1', 'gwei'),
		'nonce': web3.eth.get_transaction_count(ganache_bank_account)}
	signed_tx = web3.eth.account.sign_transaction(
		tx, bank_private_key)
	tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
	web3.eth.wait_for_transaction_receipt(tx_hash)
	print("balance Bakn: ",web3.eth.get_balance(ganache_bank_account))
	print("Balance new account: ",web3.eth.get_balance(address_account))
	return address_account, private_key


def execute_contract(web3:Web3, wallet, private_key):
	contract = web3.eth.contract(abi=abi, bytecode=bytecode)
	first_place = "test1"
	second_place = "test2"
	third_place = "test3"
	organizer = "tesst1"
	start_date_iso = datetime.now(EuropeZone).isoformat()
	start_date = datetime.fromisoformat(start_date_iso)
	start_date_int = int(start_date.timestamp())
	start_date_int = 12345
	tx = contract.constructor(first_place, second_place, third_place, organizer, start_date_int).build_transaction({
            'from': wallet,
        				'nonce': web3.eth.get_transaction_count(wallet),
        				'gas': 2000000,  # Límite de gas
        				'gasPrice': web3.to_wei('20', 'gwei')  # Precio del gas
        })
	signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)
	tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
	response = web3.eth.wait_for_transaction_receipt(tx_hash)
	print ('Contract executed: %s', response)
	contractAddress = response['contractAddress'].lower()
	print(contractAddress)
	contract_addr = web3.to_checksum_address(contractAddress)
	return contract_addr

def get_data_from_contract(web3, contract_addr):
	if not web3.is_address(contract_addr):
		print("Invalid contract address: %s", contract_addr)
	print('Contract address: %s', contract_addr)
	code = web3.eth.get_code(contract_addr)
	print('Contract code: %s', code)
	# ABI del contrato (exportada al compilar el contrato en Remix/Hardhat/Truffle)
	contract = web3.eth.contract(address=contract_addr, abi=abi)
	print('Contract: %s', contract)
#	event_signature_hash = web3.keccak(text="DataUpdated(uint256,string)").hex()
#	logs = web3.eth.get_logs({
#	    "fromBlock": 0,          # Start block for the filter
#	    "toBlock": "latest",     # End block for the filter
#	    "topics": [event_signature_hash]
#	})
#	for log in logs:
#	    event_data = contract.events.DataUpdated().processLog(log)
#	    print("The daata event is:", event_data['args'])
	dato1,dato2,dato3,dato4,dato5,dato6 = contract.functions.getTournamentResults().call()
	print('Results: %s', results)
	my_data = json.dumps({
		'first_place': results[0],
		'second_place': results[1],
		'third_place': results[2],
		'organizer': results[3],
		'start_date': results[4]
	})
	print ('Results obtained', my_data)

web3 = connect_to_blockchain()
wallet, private_key = create_account(web3)
contract_addr = execute_contract(web3, wallet, private_key)
get_data_from_contract(web3, contract_addr)