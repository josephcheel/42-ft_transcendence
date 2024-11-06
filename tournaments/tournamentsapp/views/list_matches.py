from tournamentsapp.wrappers import require_get, user_is_authenticated, validate_credentials
from tournamentsapp.models import Matches
from datetime import datetime
from django.db import OperationalError
from django.http import JsonResponse
from django.db.models import Q
import json

from user.models import User

@require_get
@validate_credentials
def list_matches(request):
	player = request.user.username
	try:
		player = User.objects.get(username=request.username)
		matches_data = Matches.objects.filter(Q(player_id1=player.id) | Q(player_id2=player.id))
		matches_list = list(matches_data.values())
		for match in matches_list:
			for key, value in match.items():
				if isinstance(value, datetime):
					match[key] = value.isoformat()
		data = json.dumps(matches_list)
		return JsonResponse({'status': 'success', 'message': 'List of matches', 'data': data}, status=200)
	except OperationalError:
		return JsonResponse({'status': 'error', 'message': 'Internal error', 'data': None}, status=500)
