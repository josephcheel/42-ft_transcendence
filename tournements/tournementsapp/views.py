from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from tournements.shared.wrappers import validate_credentials, require_post, require_get
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.core.serializers import serialize
from django.db import OperationalError
import json
from .models import Tournements, Invitations, Matches
from .status_options import StatusTournements, StatusInvitations, StatusMatches, Rounds
from django.db.models import F
try: 
	from usermodel.models import User
except:
	pass
import math

User = get_user_model()

# Create your views here.
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
def open_tournement(request):
	player = request.username
	try:
		player_owner = User.objects.get(username=player)
	except User.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'A user does not exist', 'data': None}, status=404)
	data = request.data
	if data.get('price_1') < 0 or data.get('price_2') < 0 or data.get('price_3') < 0:
		return JsonResponse({'status': 'error', 'message': 'Prices must be positive', 'data': None}, status=400)
	if data.get('price_1') < data.get('price_2') or data.get('price_2') < data.get('price_3'):
		return JsonResponse({'status': 'error', 'message': 'Invalid prices. Must be Price 1 > Price 2 > Price 3', 'data': None}, status=400)
	data_players = data.get('players')
	nr_of_players = 0
	for player in data_players:
		nr_of_players  += 1
		try:
			player_reg = User.objects.get(username=player)
		except User.DoesNotExist:
			return JsonResponse({'status': 'error', 'message': 'A player does not exist', 'data': None}, status=404)
	if nr_of_players & 1:
		return JsonResponse({'status': 'error', 'message': 'The number of players must be even', 'data': None}, status=400)
	if nr_of_players != 2 and nr_of_players < 4:
		return JsonResponse({'status': 'error', 'message': 'The number of players must be 2 or at least 4', 'data': None}, status=400)
	nr_of_rounds, extra_round = math.modf(math.log2(nr_of_players))
	if extra_round > 0:
		nr_of_rounds += 1
	tournement_created = Tournements.objects.create(
		player_id = player_owner.id, 
		date_start = data.get('Date_start'),
		date_max_end = data.get('Date_max_end'), 
		max_players = data.get('max_players'), 
		cost = data.get('cost'),
		current_round = nr_of_rounds,
		price1 = data.get('price_1'), 
		price2 = data.get('price_2'), 
		price3 = data.get('price_3'), 
		status = StatusTournements.OPEN_TOURNEMENT)
	for player in data_players:
		player_reg = User.objects.get(username=player)
		Invitations.objects.create(tournement_id = tournement_created.id, player_id = player_reg.id, price = player.get('price'))
	return JsonResponse({'status': 'success', 'message': 'Tournement created successfully', 'data': None}, status=200)

@csrf_exempt
@require_post
@validate_credentials
def accept_invitation(request):
	player = request.username
	try:
		player = User.objects.get(username=player)
	except User.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'A user does not exist', 'data': None}, status=404)
	tournement_id = request.data.get('tournement_id')
	try:
		tournement = Tournements.objects.get(id=tournement_id)
	except Tournements.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'A tournement does not exist', 'data': None}, status=404)
	try:
		invitation = Invitations.objects.get(tournement_id=tournement.id, player_id=player.id)
	except Invitations.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'You have not been invited to this tournement', 'data': None}, status=400)
	if User.objects.get(id = player.id).puntos < tournement.price:
		return JsonResponse({'status': 'error', 'message': 'You do not have enough points to accept the invitation', 'data': None}, status=400)
	status_invitations = StatusInvitations()
	if invitation.status == status_invitations.INVITATION_ACCEPTED:
		return JsonResponse({'status': 'error', 'message': 'The invitation has already been accepted', 'data': None}, status=400)
	User.objects.filter(id = player.id).update(puntos_reservados= F('puntos_reservados') + tournement.price)
	User.objects.filter(id = player.id).update(puntos= F('puntos_reservados') - tournement.price)
	invitation.status = 1
	invitation.save()
	return JsonResponse({'status': 'success', 'message': 'Invitation accepted successfully', 'data': None}, status=200)

@csrf_exempt
@require_post
@validate_credentials
def close_tournement(request):
	player = request.username
	try:
		player_owner = User.objects.get(username=player)
	except User.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'A user does not exist', 'data': None}, status=404)
	tournement_id = request.data.get('tournement_id')
	try:
		tournement = Tournements.objects.get(id=tournement_id)
	except Tournements.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'A tournement does not exist', 'data': None}, status=404)
	if tournement.player_id != player_owner.id:
		return JsonResponse({'status': 'error', 'message': 'You are not the owner of this tournement', 'data': None}, status=403)
	if tournement.status != 0:
		return JsonResponse({'status': 'error', 'message': 'The tournement is not open', 'data': None}, status=400)
	tournement_players = Invitations.objects.filter(tournement_id=tournement_id, status=StatusInvitations.ACCEPTED)
	if len(tournement_players) & 1:
		return JsonResponse({'status': 'error', 'message': 'The number of players accpted must be even', 'data': None}, status=400)
	if len(tournement_players) != 2 and len(tournement_players) < 4:
		return JsonResponse({'status': 'error', 'message': 'The number of players does not permit start tournement', 'data': None}, status=400)
	tournement.status = 1
	tournement.save()
	player_nr = len(tournement_players)
	current_round, extra_round = math.modf(math.log2(len(tournement_players)))
	if extra_round > 0:
		extra_round = 1
	for player in tournement_players:
		if not (player_nr & 1):
			match len(tournement_players):
				case 2:
					typeRound = Rounds.FINAL_ROUND
				case 4:
					typeRound = Rounds.SEMIFINAL_ROUND
				case _:
					typeRound = Rounds.QUALIFIED_ROUND
					
			current_match = Matches.objects.create(
				tournement_id = tournement_id, 
				number_round = current_round + extra_round, 
				player_id_1 = player.id, 
				player_id_2 = player.id, 
				round = typeRound)		
		else:
			current_match.player_id_2 = player.id
			current_match.save()
		User.objects.filter(id = player.id).update(puntos_reservados= F('puntos_reservados') - tournement.cost)
		player_nr -= 1
		if math.power(2, current_round ) == player_nr:
			extra_round = 0
	tournement_players.objects.delete()
	return JsonResponse({'status': 'success', 'message': 'Tournement opened successfully', 'data': None}, status=200)

@csrf_exempt
@require_post
@validate_credentials
def finish_tournement(request):
	player = request.username
	try:
		player_owner = User.objects.get(username=player)
	except User.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'A user does not exist', 'data': None}, status=404)
	tournement_id = request.data.get('tournement_id')
	try:
		tournement = Tournements.objects.get(id=tournement_id)
	except Tournements.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'A tournement does not exist', 'data': None}, status=404)
	if tournement.player_id != player_owner.id:
		return JsonResponse({'status': 'error', 'message': 'You are not the owner of this tournement', 'data': None}, status=403)
	status_tournements = StatusTournements()
	if tournement.status != status_tournements.OPEN_TOURNEMENT:
		return JsonResponse({'status': 'error', 'message': 'The tournement is not open', 'data': None}, status=400)
	tournement.status = status_tournements.CLOSED_TOURNEMENT
	pending_matches = Matches.objects.filter(tournement_id = tournement.id, status = StatusMatches.NOT_PLAYED)
	if len(pending_matches):
		return JsonResponse({'status': 'error', 'message': 'There are still pending matches', 'data': None}, status=400)
	list_of_matches = Matches.objects.filter(tournement_id=tournement.id)
	for match in list_of_matches:
		if match.round == Rounds.FINAL_ROUND:
			tournement.id_winner = match.winner_id
			tournement.id_second = match.looser_id
			User.objects.filter(id = tournement.winner).update(puntos= F('puntos') + tournement.price_1)
			User.objects.filter(id = tournement.second).update(puntos= F('puntos') + tournement.price_2)
		elif match.round == Rounds.THIRD_PLACE_ROUND:
			tournement.id_third = match.winner_id
			User.objects.filter(id = tournement.id_third).update(puntos= F('puntos') + tournement.price_3)
	tournement.status = status_tournements.FINISHED_TOURNEMENT
	tournement.save()
	return JsonResponse({'status': 'success', 'message': 'Tournement closed successfully', 'data': None}, status=200)

@csrf_exempt
@require_post
def start_match(request):
	player = request.username
	try:
		player = User.objects.get(username=player)
	except User.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'A user does not exist', 'data': None}, status=404)
	match_id = request.data.get('match_id')
	try:
		match = Matches.objects.get(match_id=match_id)
	except Matches.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'A match does not exist', 'data': None}, status=404)
	if match.player_id_1 != player.id and match.player_id_2 != player.id:
		return JsonResponse({'status': 'error', 'message': 'You are not a player of this match', 'data': None}, status=403)
	if match.status == StatusMatches.PLAYED:
		return JsonResponse({'status': 'error', 'message': 'The match has already been played', 'data': None}, status=400)
	match.status = StatusMatches.STARTED
	match.save()
	return JsonResponse({'status': 'success', 'message': 'Match started successfully', 'data': None}, status=200)

@csrf_exempt
@require_post
def finish_match(request):
	match_id = request.data.get('match_id')
	try:
		match = Matches.objects.get(match_id=match_id)
	except Matches.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'A match does not exist', 'data': None}, status=404)
	winner = request.data.get('winner')
	looser = request.data.get('looser')
	try:
		winner = User.objects.get(username=winner)
		looser = User.objects.get(username=looser)
	except User.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'A plyer 1 or 2 does not exist', 'data': None}, status=404)
	if (match.player_id_1 != winner.id and match.player_id_2 != winner.id) or (match.player_id_1 != looser.id and match.player_id_2 != looser.id):
		return JsonResponse({'status': 'error', 'message': 'You are not a player of this match', 'data': None}, status=403)
	if match.status == StatusMatches.PLAYED:
		return JsonResponse({'status': 'error', 'message': 'The match has already been played', 'data': None}, status=400)
	match.winner_id = winner.id
	match.looser_id = looser.id
	match.status = StatusMatches.PLAYED
	match.save()
	try:
		tournement = Tournements.objects.get(id=match.tournement_id, status=StatusMatches.NOT_PLAYED)
	except Tournements.DoesNotExist:
		winner.puntos = F('puntos') + 100
		return JsonResponse({'status': 'error', 'message': 'Free play finished', 'data': None}, status=200)
	if match.round == Rounds.FINAL_ROUND:
		tournement = Tournements.objects.get(id=match.tournement_id)
		tournement.id_winner = match.winner_id
		tournement.id_second = match.looser_id
	elif match.round == Rounds.THIRD_PLACE_ROUND:
		tournement = Tournements.objects.get(id=match.tournement_id)
		tournement.id_third = match.winner_id
	elif match.round == Rounds.SEMIFINAL_ROUND:
		next_match = Matches.objects.get(tournement_id=match.tournement_id, round=Rounds.SEMIFINAL_ROUND, status=StatusMatches.PLAYED)
		if len(next_match)  == 2:
			Matches.objects.create(tournement_id=match.tournement_id, player_id_1=next_match[0].winner_id, 
						  player_id_2=next_match[1].winner_id, round=Rounds.FINAL_ROUND)
			Matches.objects.create(tournement_id=match.tournement_id, player_id_1=next_match[0].looser_id, 
						  player_id_2=next_match[1].looser_id, round=Rounds.THIRD_PLACE_ROUND)
	elif match.round == Rounds.QUALIFIED_ROUND:
		if len(Matches.objects.filter(tournement_id=match.tournement_id, round=Rounds.QUALIFIED_ROUND, 
								number_round = tournement.current_round, status=StatusMatches.NOT_PLAYED)) == 0:
			tournement.current_round -= 1
			tournement.save()
			list_of_matches = Matches.objects.filter(tournement_id=match.tournement_id, round=Rounds.QUALIFIED_ROUND, 
											number_round = tournement.current_round, status=StatusMatches.PLAYED) == 0
			for i in range(0, len(list_of_matches), 2):
				Matches.objects.create(
					tournement_id=match.tournement_id, 
					player_id_1=list_of_matches[i].winner_id, 
					player_id_2=list_of_matches[i+1].winner_id, 
					round=Rounds.QUALIFIED_ROUND if tournement.current_round == 2 else Rounds.SEMIFINAL_ROUND)
	return JsonResponse({'status': 'success', 'message': 'Match finished successfully', 'data': None}, status=200)