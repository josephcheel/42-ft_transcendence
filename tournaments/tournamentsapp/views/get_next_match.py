from tournamentsapp.wrappers import require_get, user_is_authenticated, exception_handler
from tournamentsapp.models import Matches, Tournaments
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

@exception_handler
@require_get
def get_next_match(request, username=None):
	try:
		if username:
			if username.isdigit():
				player = User.objects.get(Q(id=int(username)))
			else:
				player = User.objects.get(Q(username=username))
		else:	
			player = User.objects.get(username=request.user)
		   
			matches_data = Matches.objects.filter(
					(Q(player_id_1=player.id) | Q(player_id_2=player.id)) & Q(player_id_2__isnull=False),
					status__in=[StatusMatches.PLAYED.value, StatusMatches.NEXT_ROUND_ASSIGNED.value])
			matches_data = matches_data.order_by('date')
			matches_list = list(matches_data.values())
			for key, value in matches_list[1].items():
				if isinstance(value, datetime):
					matches_list[key] = value.isoformat()
			data = json.dumps(matches_list[1])
			return JsonResponse({'status': 'success', 'message': 'List of matches', 'data': data}, status=200)
	except OperationalError:
		return JsonResponse({'status': 'error', 'message': 'Internal error', 'data': None}, status=500)
