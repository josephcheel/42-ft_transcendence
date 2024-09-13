from tournamentsapp.wrappers import validate_credentials, require_post, user_is_authenticated
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
@validate_credentials
def close_tournament(request):
	data = request.data

	tournament_id = data.get("tournament_id")
	try:
		tournament = Tournaments.objects.get(id=tournament_id)
	except Tournaments.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'A tournament does not exist', 'data': None}, status=404)

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
				player_id_1 = tournament_players[0].player_id, 
				player_id_2=tournament_players[1].player_id,
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
				player_id_1=tournament_players[0].player_id,
				player_id_2=tournament_players[1].player_id,
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
			players_round_low = int(math.pow(2, current_round + extra_round) - len(tournament_players))
			print('----------------------------')
			print('current round = ', current_round, 'extra round = ',
			      extra_round, 'players_round_low = ', players_round_low, 'tournament players = ' ,len(tournament_players))
			print('----------------------------')
			if current_round + extra_round == 3:
				round_type = Rounds.SEMIFINAL_ROUND.value
			else:
				round_type = Rounds.QUALIFIED_ROUND.value
			tournament.current_round = current_round + extra_round
			tournament.save()
			if extra_round:
				for i in range(players_round_low, len(tournament_players), 2):
					Matches.objects.create(
						tournament_id=tournament_id,
						number_round=current_round + extra_round,
						date_time=next_match_date,
						player_id_1=tournament_players[i].player_id,
						player_id_2=tournament_players[i + 1].player_id,
						round=round_type)
					player1 = User.objects.get(id=tournament_players[i].player_id)
					player1.puntos_reservados -= tournament.cost
					player2 = User.objects.get(id=tournament_players[i + 1].player_id)
					player2.puntos_reservados -= tournament.cost
			next_match_date += timedelta(minutes=5)
			if current_round == 3:
				round_type = Rounds.SEMIFINAL_ROUND.value
			else:
				round_type = Rounds.QUALIFIED_ROUND.value
			for i in range(0, players_round_low, 2):
				Matches.objects.create(
					tournament_id=tournament_id,
					date_time=next_match_date,
					number_round=current_round,
					player_id_1=tournament_players[i].player_id,
					player_id_2=tournament_players[i + 1].player_id,
					round=round_type)
				player1 = User.objects.get(id=tournament_players[i].player_id)
				player1.puntos_reservados -= tournament.cost
				player2 = User.objects.get(id=tournament_players[i + 1].player_id)
				player2.puntos_reservados -= tournament.cost
				next_match_date += timedelta(minutes=5)
	tournament.last_match_date =  next_match_date
	tournament.save()
	tournament_players = Invitations.objects.filter(tournament_id=tournament_id)
	tournament_players.delete()
	return JsonResponse({'status': 'success', 'message': 'Tournament closed successfully', 'data': None}, status=200)
