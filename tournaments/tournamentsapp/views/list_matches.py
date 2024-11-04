from tournamentsapp.wrappers import require_get, user_is_authenticated, validate_credentials
from tournamentsapp.models import Matches
from datetime import datetime
from django.db import OperationalError
from django.http import JsonResponse
import json
import logging
from django.db.models import Q
from user.models import User
logger = logging.getLogger('django')
logger.setLevel(logging.DEBUG)

@require_get
def list_matches(request, username=None):
	logger.debug(request.user)
	try:
#		try:
#			player = User.objects.get(username=player)
#		except User.DoesNotExist:
#			return JsonResponse({'status': 'error', 'message': 'A user does not exist', 'data': None}, status=404)
		if username:
			player = User.objects.get(Q(username=username) | Q(id=username))
		else:	
			player = User.objects.get(username=request.user)
		matches_data = Matches.objects.filter(
    		Q(player_id_1=player.id) | Q(player_id_2=player.id)
)
		matches_list = list(matches_data.values())
		for match in matches_list:
			for key, value in match.items():
				if isinstance(value, datetime):
					match[key] = value.isoformat()
		data = json.dumps(matches_list)
		return JsonResponse({'status': 'success', 'message': 'List of tournaments', 'data': data}, status=200)
	except OperationalError:
		return JsonResponse({'status': 'error', 'message': 'Internal error', 'data': None}, status=500)
