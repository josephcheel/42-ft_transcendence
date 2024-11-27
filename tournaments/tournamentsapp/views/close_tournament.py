from tournamentsapp.wrappers import require_post, user_is_authenticated, validate_json
from django.http import JsonResponse
from tournamentsapp.models import Tournaments, Invitations, Matches
from tournamentsapp.status_options import StatusTournaments, StatusInvitations, Rounds, StatusMatches
from datetime import timedelta
from django.utils import timezone
from tournaments.settings import TIME_DELTA
import math
import uuid
from user.models import User

@require_post
@user_is_authenticated
@validate_json
def close_tournament(request):
	data = request.data

	tournament_id = data.get("tournament_id")
	try:
		tournament = Tournaments.objects.get(id=tournament_id)
	except Tournaments.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'The tournament does not exist', 'data': None}, status=404)

	player = request.user
	if tournament.player_id != player:
		return JsonResponse({'status': 'error', 'message': 'You are not the owner of this tournament', 'data': None}, status=403)

	if tournament.status != StatusTournaments.OPEN_TOURNAMENT.value:
		return JsonResponse({'status': 'error', 'message': 'The tournament is not open', 'data': None}, status=400)

	tournament_players = Invitations.objects.filter(tournament_id=tournament_id, status=StatusInvitations.INVITATION_ACCEPTED.value)
	if len(tournament_players) < 2 :
		return JsonResponse({'status': 'error', 'message': 'The number of players accpted must grater than 1', 'data': None}, status=400)

	tournament.status = StatusTournaments.CLOSED_TOURNAMENT.value
	next_match_date = tournament.last_match_date
	player_nr = len(tournament_players)
	extra_round, current_round = math.modf(math.log2(player_nr))
	tournament.last_match_date = timezone.now() + timedelta(minutes=TIME_DELTA * 1.5 * pow(2, current_round + 1) / 2)
	tournament.save()
	if extra_round > 0:
		extra_round = 1
	match len(tournament_players):
		case 2:
			Matches.objects.create(
				tournament_id = tournament_id, 
				number_round = 1, 
				date_time = next_match_date,
				player_id_1 = tournament_players[0].player_id,
				points_winner = tournament.winning_points,
				player_id_2 = tournament_players[1].player_id,
				round=Rounds.FINAL_ROUND.value,
				match_UUID = uuid.uuid4(),
				tournament_UUID = tournament.UUID)
			tournament_players[0].player_id.puntos_reservados -= tournament.cost
			tournament_players[0].player_id.save()
			tournament_players[1].player_id.puntos_reservados -= tournament.cost
			tournament_players[1].player_id.save()
			tournament.current_round = 1
		case 4:
			Matches.objects.create(
				tournament_id = tournament_id,
				number_round = 2,
				date_time = next_match_date,
				player_id_1 = tournament_players[0].player_id,
				player_id_2 = tournament_players[1].player_id,
				points_winner=tournament.winning_points,
				round=Rounds.SEMIFINAL_ROUND.value,
				match_UUID = uuid.uuid4(),
				tournament_UUID = tournament.UUID)
			tournament_players[0].player_id.puntos_reservados -= tournament.cost
			tournament_players[0].player_id.save()
			tournament_players[1].player_id.puntos_reservados -= tournament.cost
			tournament_players[1].player_id.save()
			next_match_date += timedelta(minutes=TIME_DELTA)
			Matches.objects.create(
				tournament_id=tournament_id,
				number_round=2,
				date_time=next_match_date,
				player_id_1=tournament_players[2].player_id,
				player_id_2=tournament_players[3].player_id,
				points_winner=tournament.winning_points,
				round=Rounds.SEMIFINAL_ROUND.value,
				match_UUID = uuid.uuid4(),
				tournament_UUID = tournament.UUID)
			tournament_players[2].player_id.puntos_reservados -= tournament.cost
			tournament_players[2].player_id.save()
			tournament_players[3].player_id.puntos_reservados -= tournament.cost
			tournament_players[3].player_id.save()
			tournament.current_round = 2
		case _:
			numero_partidos = int(math.pow(2, current_round + extra_round -1)) 
			for i in range (0, numero_partidos):
				tournament_players[i].player_id.puntos_reservados -= tournament.cost
				tournament_players[i].player_id.save()
				try:
					player_2 = tournament_players[i + numero_partidos].player_id
					player_2.puntos_reservados  -= tournament.cost
					player_2.save()
					status = StatusMatches.NOT_PLAYED.value
					player_winner = None
				except:
					player_2 = None
					player_winner = tournament_players[i].player_id
					status = StatusMatches.WALKOVER.value

				Matches.objects.create(
					tournament_id = tournament_id,
					date_time = next_match_date,
					player_id_1 = tournament_players[i].player_id,
					player_id_2 = player_2,
					winner_id = player_winner,
                    points_winner=tournament.winning_points,
					round=Rounds.QUALIFIED_ROUND.value,
					number_round = current_round + extra_round,
					status=status,
					match_UUID = uuid.uuid4(),
					tournament_UUID = tournament.UUID)
				next_match_date += timedelta(minutes=TIME_DELTA)
			tournament.current_round = current_round + extra_round
	tournament.last_match_date =  next_match_date
	tournament.save()
	tournament_players = Invitations.objects.filter(tournament_id=tournament_id)
	tournament_players.delete()
	return JsonResponse({'status': 'success', 'message': 'Tournament closed successfully', 'data': None}, status=200)
