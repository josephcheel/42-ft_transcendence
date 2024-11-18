from django.urls import path
from blockchainapp.views import execute_contract, get_balance, make_transaction, get_results_from_blockchain

urlpatterns = [
	path('get_balance/', get_balance),
	path('make_transaction/', make_transaction),
	path('get_results_from_blockchain/', get_results_from_blockchain),
]