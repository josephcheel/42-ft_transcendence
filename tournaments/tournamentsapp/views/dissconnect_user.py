from tournamentsapp.wrappers import require_post, validate_json
from django.http import JsonResponse
import json
from tournamentsapp.models import Tournaments, Matches
from tournamentsapp.status_options import  StatusMatches, StatusTournaments
from tournamentsapp.tasks.actualise_tournaments import actualise_tournament
from django.utils import timezone
from datetime import timedelta
from user.models import User
import logging

logger = logging.getLogger('django')

@require_post
@validate_json
def disconnect_user(request):
	data = request.data
	player = request.user
	match_UUId = request.data.get('UUID')
	mymatch = Matches.objects.get(match_UUID=match_UUId)
	if mymatch.status == StatusMatches.WAITING_PLAYER1.value or mymatch.status == StatusMatches.WAITING_PLAYER2.value:
		mymatch.status = StatusMatches.NOT_PLAYED.value
		mymatch.save()
		return JsonResponse({'status': 'error', 'message': 'The match status changed to not played', 'data': None}, status=200)
	return JsonResponse({'status': 'success', 'message': 'Match is playing', 'data': None}, status=400)