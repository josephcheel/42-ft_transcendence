from ..wrappers import validate_credentials, require_post, require_get, user_is_authenticated
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.core.serializers import serialize
from django.db import OperationalError
import json
from ..models import Tournaments, Invitations, Matches
from ..status_options import StatusTournaments, StatusInvitations, StatusMatches, Rounds
from datetime import datetime, timedelta
from django.utils import timezone



try: 
	from usermodel.models import User
except:
	from ..models import User
import math

def list_of_matches(request):
	if request.method == 'GET':
		player = request.username
		try:
			try:
				player = User.objects.get(username=player)
			except User.DoesNotExist:
				return JsonResponse({'status': 'error', 'message': 'A user does not exist', 'data': None}, status=404)
			tournaments = Tournaments.objects.filter(player_id=player)
			data = serialize('json', tournaments)
			data = json.loads(data)
			data = [entry['fields'] for entry in data]
			return JsonResponse({'status': 'success', 'message': 'List of tournaments', 'data': data}, status=200)
		except OperationalError:
			return JsonResponse({'status': 'error', 'message': 'Internal error', 'data': None}, status=500)
	else:
		return JsonResponse({'status': 'error', 'message': 'Invalid request method GET for list of tournaments', 'data': None}, status=400)

@require_post
@validate_credentials
def open_tournament(request):
	player = request.username
	try:
		player_owner = User.objects.get(username=player)
	except User.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'The owner user does not exist', 'data': None}, status=400)
	data = request.data

	received_date_start = datetime.fromisoformat(str(data.get('date_start')))
	if received_date_start < timezone.now():
		return JsonResponse({'status': 'error', 'message': 'Invalid start date', 'data': None}, status=400)

	if data.get('max_players') & 1:
		return JsonResponse({'status': 'error', 'message': 'The max number of players must be even', 'data': None}, status=400)

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
			return JsonResponse({'status': 'error', 'message': 'One invited player does not exist', 'data': None}, status=400)
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
		player_id = player_owner.id, 
		date_start=received_date_start,
		last_match_date=received_date_start,
		date_max_end=received_date_start + timedelta(minutes=nr_of_matches * 5 + 30),
		max_players = data.get('max_players'), 
		cost = data.get('cost'),
		current_round = nr_of_rounds + extra_round,
		price_1 = data.get('price_1'), 
		price_2 = data.get('price_2'), 
		price_3 = data.get('price_3'), 
		id_winner = 0,
		id_second = 0,
		id_third = 0,
		status=StatusTournaments.OPEN_TOURNAMENT.value)
	for player in data_players:
		player_reg = User.objects.get(username=player)
		Invitations.objects.create(tournament_id=tournament_created.id, player_id=player_reg.id, status=StatusInvitations.INVITATION_IGNORED.value)
	return JsonResponse({'status': 'success', 'message': 'Tournament created successfully', 'data': None}, status=200)

@require_post
@validate_credentials
def accept_invitation(request):
	data = request.data
	tournament = data.get("tournament_id")
	try:
		tournament = Tournaments.objects.get(id=tournament)
	except Tournaments.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'The tournament does not exist', 'data': None}, status=400)

	player = data.get("username")
	try: 
		player = User.objects.get(username=player)
	except User.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'The user does not exist', 'data': None}, status=400)

	try:
		invitation = Invitations.objects.get(tournament_id=tournament.id, player_id=player.id)
	except Invitations.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'You have not been invited to this tournament', 'data': None}, status=400)
	if player.puntos < tournament.cost:
		return JsonResponse({'status': 'error', 'message': 'You do not have enough points to accept the invitation', 'data': None}, status=400)
	if invitation.status == StatusInvitations.INVITATION_ACCEPTED.value:
		return JsonResponse({'status': 'error', 'message': 'The invitation has already been accepted', 'data': None}, status=400)
	player.puntos_reservados +=tournament.cost
	player.puntos -= tournament.cost
	player.save()
	invitation.status = StatusInvitations.INVITATION_ACCEPTED.value
	invitation.save()
	return JsonResponse({'status': 'success', 'message': 'Invitation accepted successfully', 'data': None}, status=200)

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

def finish_tournament(tournament_id):
	tournament = Tournaments.objects.get(id=tournament_id)
	list_of_matches = Matches.objects.filter(tournament_id=tournament.id)
	for match in list_of_matches:
		if match.round == Rounds.FINAL_ROUND.value:
			tournament.id_winner = match.winner_id
			tournament.id_second = match.looser_id
			user = User.objects.get(id = tournament.id_winner)
			user.puntos += tournament.price_1
			user.save()
			user = User.objects.get(id = tournament.id_second)
			user.puntos += tournament.price_2
			user.save()
		elif match.round == Rounds.THIRD_PLACE_ROUND.value:
			tournament.id_third = match.winner_id
			user = User.objects.get(id=tournament.id_third)
			user.puntos += tournament.price_3
			user.save()
	tournament.status = StatusTournaments.FINISHED_TOURNAMENT.value
	tournament.save()

@require_post
def start_match(request):
	request.data = json.loads(request.body)
	try:
		request.data = json.loads(request.body)
	except json.JSONDecodeError:
		return JsonResponse({'status': 'error', 'message': 'Invalid JSON body', 'data': None}, status=400)
	data = request.data
	player = data.get('player')
	try:
		player = User.objects.get(username=player)
	except User.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'A user does not exist', 'data': None}, status=404)
	match_id = data.get('match_id')
	try:
		match = Matches.objects.get(match_id=match_id)
	except Matches.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'A match does not exist', 'data': None}, status=404)
	if match.player_id_1 != player.id and match.player_id_2 != player.id:
		return JsonResponse({'status': 'error', 'message': 'You are not a player of this match', 'data': None}, status=403)
	if match.status == StatusMatches.PLAYED.value:
		return JsonResponse({'status': 'error', 'message': 'The match has already been played', 'data': None}, status=400)
	match.status = StatusMatches.STARTED.value
	match.save()
	return JsonResponse({'status': 'success', 'message': 'Match started successfully', 'data': None}, status=200)

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
