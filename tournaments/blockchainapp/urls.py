from django.urls import path
from blockchainapp.views import connection

urlpatterns = [
	path('connect/', connection),
]