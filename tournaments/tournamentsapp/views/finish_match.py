from tournamentsapp.wrappers import require_post, validate_json
from django.http import JsonResponse
import json
from tournamentsapp.models import Tournaments, Matches
from tournamentsapp.status_options import  StatusMatches, Rounds
from tournamentsapp.tasks.actualise_tournaments import actualise_tournament

try: 
	from usermodel.models import User
except:
	from ..models import User

@require_post
@validate_json
def finish_match(request):
	data = request.data
	match_id = request.data.get('match_id')
	try:
		match = Matches.objects.get(id=match_id)
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
	match.status = StatusMatches.PLAYED.value
	match.save()

	try:
		tournament = Tournaments.objects.get(id=match.tournament_id)
	except Tournaments.DoesNotExist:
		winner.puntos += 100
		return JsonResponse({'status': 'error', 'message': 'Free play finished', 'data': None}, status=200)
	actualise_tournament(match)

	return JsonResponse({'status': 'success', 'message': 'Match finished successfully', 'data': None}, status=200)
