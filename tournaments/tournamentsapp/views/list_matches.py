from tournamentsapp.wrappers import require_get, user_is_authenticated, exception_handler
from tournamentsapp.models import Matches
from tournamentsapp.status_options import StatusMatches
from datetime import datetime
from django.db import OperationalError
from django.http import JsonResponse
from django.db.models import Q
import json
import logging
from django.db.models import Q
from user.models import User
logger = logging.getLogger('django')
logger.setLevel(logging.DEBUG)

@require_get
@exception_handler
def list_matches(request, username=None):
	logger.debug(request.user)
	try:
		if username:
			if username.isdigit():
				player = User.objects.get(Q(id=int(username)))
			else:
				player = User.objects.get(Q(username=username))
		else:	
			player = User.objects.get(username=request.user)
		matches_data = Matches.objects.filter(
                    Q(player_id_1=player.id) | Q(player_id_2=player.id), 
					Q(status=StatusMatches.PLAYED) | Q(status=StatusMatches.NEXT_ROUND_ASSIGNED))
    #player = request.user.username
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


@require_get
@exception_handler
def list_not_played_matches(request, username=None):
	logger.debug(request.user)
	try:
		if username:
			if username.isdigit():
				player = User.objects.get(Q(id=int(username)))
			else:
				player = User.objects.get(Q(username=username))
		else:
			player = User.objects.get(username=request.user)
		matches_data = Matches.objects.filter(
                    Q(player_id_1=player.id) | Q(player_id_2=player.id),
               		status=StatusMatches.NOT_PLAYED)
    # player = request.user.username
		matches_list = list(matches_data.values())
		for match in matches_list:
			for key, value in match.items():
				if isinstance(value, datetime):
					match[key] = value.isoformat()
		data = json.dumps(matches_list)
		return JsonResponse({'status': 'success', 'message': 'List of matches', 'data': data}, status=200)
	except OperationalError:
		return JsonResponse({'status': 'error', 'message': 'Internal error', 'data': None}, status=500)
