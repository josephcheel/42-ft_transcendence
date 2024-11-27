from tournamentsapp.wrappers import require_post, user_is_authenticated, validate_json
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.utils import timezone
import math
from tournamentsapp.models import Tournaments, Invitations
from tournamentsapp.status_options import StatusTournaments, StatusInvitations
from tournaments.settings import TIME_DELTA
from django.views.decorators.csrf import csrf_exempt
import logging
import uuid

from user.models import User

logger = logging.getLogger('django')
logger.setLevel(logging.DEBUG)

@require_post
@user_is_authenticated
@validate_json
def open_tournament(request):
	player_owner = request.user
	data = request.data

	received_date_start = datetime.fromisoformat(str(data.get('date_start')))
	if received_date_start < timezone.now():
		return JsonResponse({'status': 'error', 'message': 'Invalid start date', 'data': None}, status=400)

#	if data.get('max_players') & 1:
#		return JsonResponse({'status': 'error', 'message': 'The max number of players must be even', 'data': None}, status=400)

	if data.get('cost') < 0 or data.get('price_1') < 0 or data.get('price_2') < 0 or data.get('price_3') < 0:
		return JsonResponse({'status': 'error', 'message': 'Prices or cost must be positive', 'data': None}, status=400)

	if data.get('price_1') < data.get('price_2') or data.get('price_2') < data.get('price_3'):
		return JsonResponse({'status': 'error', 'message': 'Invalid prices. Must be Price 1 > Price 2 > Price 3', 'data': None}, status=400)

	data_players = data.get('players')
	nr_of_players = 0
	for player in data_players:
		nr_of_players  += 1
		try:
			player_reg = User.objects.get(username=player)
		except User.DoesNotExist:
			player_reg = User.objects.get(username=player)
			return JsonResponse({'status': 'error', 'message': f'The player with name: {player}, does not exist', 'data': None}, status=400)
	if nr_of_players != 2 and nr_of_players < 4:
		return JsonResponse({'status': 'error', 'message': 'The number of players must be 2 or at least 4', 'data': None}, status=400)
	extra_round, nr_of_rounds = math.modf(math.log2(nr_of_players))
	nr_of_rounds = int(nr_of_rounds)
	if extra_round > 0:
		extra_round = 1
	nr_of_matches = 0
	for i in range(0, nr_of_rounds):
		nr_of_matches += math.pow(2, i)
	nr_of_matches += int(math.pow(2, nr_of_rounds + extra_round) - nr_of_players)
	tournament_created = Tournaments.objects.create(
		player_id = player_owner, 
		date_start=received_date_start,
		last_match_date=received_date_start,
		date_max_end=received_date_start + timedelta(minutes=nr_of_matches * TIME_DELTA + 30),
		name = data.get('name'),
		winning_points = data.get('winning_points'),
		max_players = data.get('max_players'), 
		cost = data.get('cost'),
		current_round = nr_of_rounds + extra_round,
		price_1 = data.get('price_1'), 
		price_2 = data.get('price_2'), 
		price_3 = data.get('price_3'), 
		id_winner = None,
		id_second = None,
		id_third = None,
		status=StatusTournaments.OPEN_TOURNAMENT.value,
		UUID = uuid.uuid4())
	for player in data_players:
		player_reg = User.objects.get(username=player)
		Invitations.objects.create(tournament_id=tournament_created, player_id=player_reg, status=StatusInvitations.INVITATION_IGNORED.value)
	return JsonResponse({'status': 'success', 'message': 'Tournament created successfully', 'data': None}, status=200)
