from tournamentsapp.wrappers import require_post, user_is_authenticated, validate_json
from django.http import JsonResponse
from tournamentsapp.models import Tournaments, Invitations, Matches
from tournamentsapp.status_options import StatusTournaments, StatusInvitations, Rounds, StatusMatches
from tournamentsapp.tasks.create_matches import CreateMatches
from datetime import timedelta
from django.utils import timezone
from tournaments.settings import TIME_DELTA
import math

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
	if tournament_players.count() < 2 :
		return JsonResponse({'status': 'error', 'message': 'The number of players accpted must grater than 1', 'data': None}, status=400)

	tournament.status = StatusTournaments.CLOSED_TOURNAMENT.value
	next_match_date = tournament.last_match_date
	player_nr = tournament_players.count()
	extra_round, current_round = math.modf(math.log2(player_nr))

	tournament.last_match_date = timezone.now() + timedelta(minutes=TIME_DELTA * 1.5 * pow(2, current_round + 1) / 2)
	tournament.save()
	if extra_round > 0:
		extra_round = 1
	next_match_date = CreateMatches(tournament_id, tournament_players, extra_round)
	tournament.last_match_date =  next_match_date
	tournament.save()
	tournament_players = Invitations.objects.filter(tournament_id=tournament_id)
	tournament_players.delete()
	return JsonResponse({'status': 'success', 'message': 'Tournament closed successfully', 'data': None}, status=200)
