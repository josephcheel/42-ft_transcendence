from django.urls import path
from blockchainapp.views import execute_contract, get_balance, make_transaction

urlpatterns = [
	path('execute_contract/', execute_contract),
	path('get_balance/', get_balance),
	path('make_transaction/', make_transaction),
]