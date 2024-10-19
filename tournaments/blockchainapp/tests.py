from django.test import TestCase
from web3 import Web3
from blockchainapp.views import connection
from django.test import Client
import json
from django.urls import reverse
# Create your views here.

class test_BlockchainTest(TestCase):
	def setUp(self):
		self.client = Client()

	def check_json(self, response, code):
		self.assertJSONEqual(json.dumps(self.base_json),
		                     response.content.decode("utf-8"))
		self.assertEqual(response.status_code, code)

	def test_connection(self):
		response = self.client.post(reverse(connection), json.dumps(
            {"account":"123456"}), content_type='application/json')
		# Verificar conexión
		print (response)
		self.assertTrue(Web3.is_connected())
