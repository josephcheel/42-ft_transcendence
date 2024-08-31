from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .wrappers import validate_credentials, require_post, require_get
from django.contrib.auth import get_user_model
from django.http import JsonResponse
import json
from .models import Tournements, matches, players
try: 
	from usermodel.models import User
except:
	pass

User = get_user_model()

# Create your views here.
def custom_404_view(request, exception=None):
	response_data = {
		'status': 'error',
		'message': 'The requested resource was not found',
		'data': None
	}
	return JsonResponse(response_data, status=404)

@csrf_exempt
@validate_credentials
def list_tournements(request):
	if request.method == 'GET':
		player = request.username
		try:
			try:
				player = User.objects.get(username=player)
			except User.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'A user does not exist', 'data': None}, status=404)
			tournements = Tournements.objects.filter(player_id=player)
			data = serialize('json', tournements)
			data = json.loads(data)
			data = [entry['fields'] for entry in data]
			return JsonResponse({'status': 'success', 'message': 'List of tournements', 'data': data}, status=200)
		except OperationalError:
			return JsonResponse({'status': 'error', 'message': 'Internal error', 'data': None}, status=500)
	else:
		return JsonResponse({'status': 'error', 'message': 'Invalid request method GET for list of tournements', 'data': None}, status=400)

@csrf_exempt
@require_post
@validate_credentials
def create_tournement(request):
	player = request.username
	try:
		player = User.objects.get(username=player)
	except User.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'A user does not exist', 'data': None}, status=404)
	data = request.data
	Tournements.objects.create(name = data.get('name'), date = data.get('Date'), max_players = data.get('max_players'), price1 = data.get('price_1'), price2 = data.get('price_2'), price3 = data.get('price_3'), status = 0)
	data_players = data.get('players')
	for player in data_players:
		player_id = User.objects.player.get(player)
		players.objects.create(name = User.objects.player.get('name'), price = player.get('price'), round = player.get('round'))

	return JsonResponse({'status': 'success', 'message': 'Tournement created successfully', 'data': None}, status=200)
	

@csrf_exempt
@require_post
@validate_credentials
def open_tournement(request):
	player = request.username


@csrf_exempt
@require_post
@validate_credentials
def close_tournement(request):
	username = request.username
	data  = request.data
	tournements = Tournements.objects.all()
	tournements_list = []
	for tournement in tournements:
		tournements_list.append({
			'name': tournement.name,
			'Date': tournement.Date,
			'max_players': tournement.max_players,
			'price_1': tournement.price_1,
			'price_2': tournement.price_2,
			'price_3': tournement.price_3,
			'winner': tournement.winner,
			'second': tournement.second,
			'third': tournement.third,
			'hashprevius': tournement.hashprevius,
			'hash': tournement.hash
		})
		return JsonResponse({'status': 'success', 'message': 'Tournements fetched successfully', 'data': tournements_list}, status=200)
	else:
		return JsonResponse({'status': 'error', 'message': 'Invalid request method', 'data': None}, status=400)