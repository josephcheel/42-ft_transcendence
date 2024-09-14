from tournamentsapp.wrappers import require_post, user_is_authenticated, validate_json
from django.http import JsonResponse
from tournamentsapp.models import Tournaments, Invitations, Matches
from tournamentsapp.status_options import StatusTournaments, StatusInvitations, Rounds
from datetime import timedelta
from django.utils import timezone

try: 
	from usermodel.models import User
except:
	from tournamentsapp.models import User
import math


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

	player = data.get("username")
	try:
		player_owner = User.objects.get(username=player)
	except User.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'A user does not exist', 'data': None}, status=404)

	if tournament.player_id != player_owner.id:
		return JsonResponse({'status': 'error', 'message': 'You are not the owner of this tournament', 'data': None}, status=403)
	if tournament.status != StatusTournaments.OPEN_TOURNAMENT.value:
		return JsonResponse({'status': 'error', 'message': 'The tournament is not open', 'data': None}, status=400)

	tournament_players = Invitations.objects.filter(tournament_id=tournament_id, status=StatusInvitations.INVITATION_ACCEPTED.value)
	if len(tournament_players) & 1:
		return JsonResponse({'status': 'error', 'message': 'The number of players accpted must be even', 'data': None}, status=400)
	if len(tournament_players) == 0:
		return JsonResponse({'status': 'error', 'message': 'The number of players is 0 and does not permit start tournament', 'data': None}, status=400)

	tournament.status = StatusTournaments.CLOSED_TOURNAMENT.value
	next_match_date = tournament.last_match_date
	player_nr = len(tournament_players)
	extra_round, current_round = math.modf(math.log2(player_nr))
	tournament.last_match_date = timezone.now() + timedelta(minutes=7 * pow(2, current_round + 1) / 2)
	tournament.save()
	if extra_round > 0:
		extra_round = 1
	match len(tournament_players):
		case 2:
			Matches.objects.create(
				tournament_id = tournament_id, 
				number_round = 1, 
				date_time = next_match_date,
				player_id_1 = tournament_players[0], 
				player_id_2 = tournament_players[1],
				round=Rounds.FINAL_ROUND.value)
			player1 = User.objects.get(id=tournament_players[0].player_id)
			player1.puntos_reservados -= tournament.cost
			player2 = User.objects.get(id=tournament_players[1].player_id)
			player2.puntos_reservados -= tournament.cost
			tournament.current_round = 2
		case 4:
			Matches.objects.create(
				tournament_id=tournament_id,
				number_round=2,
				date_time=next_match_date,
				player_id_1=tournament_players[0],
				player_id_2=tournament_players[1],
				round=Rounds.SEMIFINAL_ROUND.value)
			player1 = User.objects.get(id=tournament_players[0].player_id)
			player1.puntos_reservados -= tournament.cost
			player2 = User.objects.get(id=tournament_players[1].player_id)
			player2.puntos_reservados -= tournament.cost
			next_match_date += timedelta(minutes=5)
			Matches.objects.create(
				tournament_id=tournament_id,
				number_round=2,
				date_time=next_match_date,
				player_id_1=tournament_players[2].player_id,
				player_id_2=tournament_players[3].player_id,
				round=Rounds.SEMIFINAL_ROUND.value)
			player1 = User.objects.get(id=tournament_players[2].player_id)
			player1.puntos_reservados -= tournament.cost
			player2 = User.objects.get(id=tournament_players[3].player_id)
			player2.puntos_reservados -= tournament.cost
			tournament.current_round = 3
			tournament.save()
		case _:
			for i in range (0, int(math.pow(2, current_round + extra_round)), 2):
				try
					player1 = User.objects.get(id=tournament_players[i])
					player1.puntos_reservados -= tournament.cost
				except User.DoesNotExist:
					player1 = None
				try:
					player2 = User.objects.get(id=tournament_players[i + 1])
					player2.puntos_reservados -= tournament.cost
				except User.DoesNotExist:
					player2 = None
				if player1 is None or player2 is None:
					match_status = Rounds.WALKOVER.value
					Matches.objects.create(
						tournament_id=tournament_id,
						number_round=1,
						date_time=next_match_date,
						player_id_1=tournament_players[i],
						player_id_2=tournament_players[i + 1],
						round=Rounds.QUALIFIED_ROUND.value,
						status = match_status)
					next_match_date += timedelta(minutes=5)
			print('----------------------------')
			print('current round = ', current_round, 'players current Round = ', current_round + extra_round, 'tournament players = ' ,len(tournament_players))
			print('----------------------------')
			tournament.current_round = current_round + extra_round
			tournament.save()
	tournament.last_match_date =  next_match_date
	tournament.save()
	tournament_players = Invitations.objects.filter(tournament_id=tournament_id)
	tournament_players.delete()
	return JsonResponse({'status': 'success', 'message': 'Tournament closed successfully', 'data': None}, status=200)
