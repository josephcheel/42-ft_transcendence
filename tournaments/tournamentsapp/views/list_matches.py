from tournamentsapp.wrappers import require_get, user_is_authenticated, exception_handler
from tournamentsapp.models import Matches
from datetime import datetime
from django.db import OperationalError
from django.http import JsonResponse
from django.db.models import Q
import json

from user.models import User

@require_get
@exception_handler
def list_matches(request, username):
    #player = request.user.username
	try:
		player = User.objects.get(username=username)
		matches_data = Matches.objects.filter(Q(player_id_1=player.id) | Q(player_id_2=player.id))
		matches_list = list(matches_data.values())
		for match in matches_list:
			for key, value in match.items():
				if isinstance(value, datetime):
					match[key] = value.isoformat()
		data = json.dumps(matches_list)
		return JsonResponse({'status': 'success', 'message': 'List of matches', 'data': data}, status=200)
	except OperationalError:
		return JsonResponse({'status': 'error', 'message': 'Internal error', 'data': None}, status=500)





@require_get
@exception_handler
def list_matches_by_tournament_id(request, tournament_id):
    # player = request.user.username
	try:
		matches_data = Matches.objects.filter(tournament_id=int(tournament_id))
		matches_list = list(matches_data.values())
		for match in matches_list:
			for key, value in match.items():
				if isinstance(value, datetime):
					match[key] = value.isoformat()
		data = json.dumps(matches_list)
		return JsonResponse({'status': 'success', 'message': 'List of matches', 'data': data}, status=200)
	except OperationalError:
		return JsonResponse({'status': 'error', 'message': 'Internal error', 'data': None}, status=500)
