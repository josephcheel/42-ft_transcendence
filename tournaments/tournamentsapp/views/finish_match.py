from tournamentsapp.wrappers import require_post, validate_json
from django.http import JsonResponse
import json
from tournamentsapp.models import Tournaments, Matches
from tournamentsapp.status_options import  StatusMatches, StatusTournaments
from tournamentsapp.tasks.actualise_tournaments import actualise_tournament
from django.utils import timezone
from user.models import User
import logging

logger = logging.getLogger('django')

@require_post
@validate_json
def finish_match(request):
	data = request.data
	match_id = request.data.get('match_id')
	if type(match_id) == int and match_id < 0:
		player1 = User.objects.get(username=data.get('winner'))
		player2 = User.objects.get(username=data.get('looser'))
		Matches.objects.create(
			number_round=0, 
			date_time=timezone.now(), 
			player_id_1=player1, 
			player_id_2=player2, 
			round=None, 
			status=StatusMatches.PLAYED.value, 
			winner_id = player1, 
			points_winner=data.get("points_winner"), 
			looser_id = player2, 
			points_looser=data.get("points_looser"),
		)
		return JsonResponse({'status': 'success', 'message': 'Match finished successfully', 'data': None}, status=200)
	try:
		match = Matches.objects.get(match_UUID=match_id)
	except Matches.DoesNotExist:
			return JsonResponse({'status': 'error', 'message': 'The match does not exist', 'data': None}, status=400)

	tournament_id = match.tournament_id
	winner = data.get('winner')
	looser = data.get('looser')
	try:
		winner = User.objects.get(username=winner)
		looser = User.objects.get(username=looser)
	except User.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'A plyer 1 or 2 does not exist', 'data': None}, status=400)
	if (match.player_id_1.id != winner.id and match.player_id_2.id != winner.id) or (match.player_id_1.id != looser.id and match.player_id_2.id != looser.id):
		return JsonResponse({'status': 'error', 'message': 'One of the players don\'t belong to this match', 'data': None}, status=400)
	if match.status == StatusMatches.PLAYED.value:
		return JsonResponse({'status': 'error', 'message': 'The match has already been played', 'data': None}, status=400)
	match.winner_id = winner
	match.looser_id = looser
	match.points_winner = data.get('points_winner')
	match.points_looser = data.get('points_looser')
	match.status = StatusMatches.PLAYED.value
	match.save()

	try:
		tournament = Tournaments.objects.get(id=match.tournament_id)
	except Tournaments.DoesNotExist:
		winner.puntos += 100
		return JsonResponse({'status': 'error', 'message': 'Free play finished', 'data': None}, status=200)
	mymatches = Matches.objects.filter(tournament_id=match.tournament_id, status__in=[StatusMatches.NOT_PLAYED.value])
	if mymatches.count() == 0:
		logger.debug(f'tournament passed to create next round: {match.id}')
		tournament.status = StatusTournaments.CREATE_NEXT_ROUND.value
		actualise_tournament(match.mytournament_id)	

	return JsonResponse({'status': 'success', 'message': 'Match finished successfully', 'data': None}, status=200)