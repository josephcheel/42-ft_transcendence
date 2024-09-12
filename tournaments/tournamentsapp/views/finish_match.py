from tournamentsapp.wrappers import require_post
from django.http import JsonResponse
import json
from tournamentsapp.models import Tournaments, Matches
from tournamentsapp.status_options import  StatusMatches, Rounds
from datetime import timedelta
from finish_tournament import finish_tournament
try: 
	from usermodel.models import User
except:
	from ..models import User

@require_post
def finish_match(request):
	request.data = json.loads(request.body)
	try:
		request.data = json.loads(request.body)
	except json.JSONDecodeError:
		return JsonResponse({'status': 'error', 'message': 'Invalid JSON body', 'data': None}, status=400)
	data = request.data
	match_id = request.data.get('match_id')
	try:
		match = Matches.objects.get(match_id=match_id)
	except Matches.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'The match does not exist', 'data': None}, status=400)
	winner = request.data.get('winner')
	looser = request.data.get('looser')
	try:
		winner = User.objects.get(username=winner)
		looser = User.objects.get(username=looser)
	except User.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'A plyer 1 or 2 does not exist', 'data': None}, status=400)
	if (match.player_id_1 != winner.id and match.player_id_2 != winner.id) or (match.player_id_1 != looser.id and match.player_id_2 != looser.id):
		return JsonResponse({'status': 'error', 'message': 'One of the players don\'t belong to this match', 'data': None}, status=400)
	if match.status == StatusMatches.PLAYED.value:
		return JsonResponse({'status': 'error', 'message': 'The match has already been played', 'data': None}, status=400)
	match.winner_id = winner.id
	match.looser_id = looser.id
	match.status = StatusMatches.PLAYED.value
	match.save()
	try:
		tournament = Tournaments.objects.get(id=match.tournament_id)
	except Tournaments.DoesNotExist:
		winner.puntos += 100
		return JsonResponse({'status': 'error', 'message': 'Free play finished', 'data': None}, status=200)
	match (match.round):
		case Rounds.FINAL_ROUND.value:
			tournament = Tournaments.objects.get(id=match.tournament_id)
			tournament.id_winner = match.winner_id
			tournament.id_second = match.looser_id
			match.status = StatusMatches.NEXT_ROUND_ASSIGNED.value
			finish_tournament(tournament.id)
		case Rounds.THIRD_PLACE_ROUND.value:
			tournament = Tournaments.objects.get(id=match.tournament_id)
			tournament.id_third = match.winner_id
			match.status = StatusMatches.NEXT_ROUND_ASSIGNED.value
		case Rounds.SEMIFINAL_ROUND.value:
			next_match = Matches.objects.filter(tournament_id=match.tournament_id,
		                                 round=Rounds.SEMIFINAL_ROUND.value, status=StatusMatches.PLAYED.value)
			if len(next_match)  == 2:
				Matches.objects.create(
								tournament_id=match.tournament_id,
								player_id_1=next_match[0].looser_id,
								player_id_2=next_match[1].looser_id,
								date_time=tournament.last_match_date + timedelta(minutes=5),
								round=Rounds.THIRD_PLACE_ROUND.value,
                                number_round=2)
				Matches.objects.create(
								tournament_id=match.tournament_id, 
								player_id_1=next_match[0].winner_id, 
								player_id_2=next_match[1].winner_id, 
								date_time = tournament.last_match_date + timedelta(minutes=10),
								round=Rounds.FINAL_ROUND.value,
                                number_round=2)
				next_match[0].status = StatusMatches.NEXT_ROUND_ASSIGNED.value
				next_match[1].status = StatusMatches.NEXT_ROUND_ASSIGNED.value
				tournament.last_match_date += timedelta(minutes=10)
				tournament.current_round -= 1
				tournament.save()
		case _:
			next_match = Matches.objects.filter(tournament_id=match.tournament_id,
										round=Rounds.QUALIFIED_ROUND.value, status=StatusMatches.PLAYED.value)
			if len(next_match) == 2:
				if tournament.current_round == 4:
					ronda_siguiente = Rounds.SEMIFINAL_ROUND.value
				else:
					ronda_siguiente = Rounds.QUALIFIED_ROUND.value
				Matches.objects.create(
							tournament_id=match.tournament_id,
							player_id_1=next_match[0].winner_id,
							player_id_2=next_match[1].winner_id,
							date_time=tournament.last_match_date +
							timedelta(minutes=5),
							round=ronda_siguiente,
                            number_round=tournament.current_round - 1)
				tournament.last_match_date += timedelta(minutes=5)
				matches_not_played = Matches.objects.filter(
					tournament_id=match.tournament_id, round=tournament.current_round, status=StatusMatches.NOT_PLAYED.value)
				if len(matches_not_played) == 0:
					tournament.current_round -= 1
				tournament.save()
	matches = Matches.objects.filter(tournament_id=match.tournament_id)
	return JsonResponse({'status': 'success', 'message': 'Match finished successfully', 'data': None}, status=200)
