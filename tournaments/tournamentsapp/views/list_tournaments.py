from tournamentsapp.wrappers import require_get, user_is_authenticated
from tournamentsapp.models import Tournaments
from datetime import datetime
from django.db import OperationalError
from django.http import JsonResponse
import json

from user.models import User

@require_get
@user_is_authenticated
def list_tournaments(request):
	player = request.user
	try:
		tournament_data = Tournaments.objects.filter(player_id=player.id)
		# Convert any datetime fields to string
		tournament_list = list(tournament_data.values())
		for tournament in tournament_list:
			for key, value in tournament.items():
				if isinstance(value, datetime):
					tournament[key] = value.isoformat()
		data = json.dumps(tournament_list)
		return JsonResponse({'status': 'success', 'message': 'List of tournaments cereated', 'data': data}, status=200)
	except OperationalError:
		return JsonResponse({'status': 'error', 'message': 'Internal error', 'data': data}, status=500)
