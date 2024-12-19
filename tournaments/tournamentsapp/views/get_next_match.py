from tournamentsapp.wrappers import require_get, user_is_authenticated, exception_handler
from tournamentsapp.models import Matches, Tournaments
from tournamentsapp.status_options import StatusMatches
from datetime import datetime, timedelta
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
			matches_list = []
			if (matches_data[1].date_time < datetime.now()+timedelta(minutes=1)):
				match = matches_data[1]
				try:
					tournament = Tournaments.objects.get(id=match.tournament_id)
					match_dict = {}
					match_dict['id']= match.id
					match_dict['player_id_1']= match.player_id_1.id if match.player_id_1 else None
					match_dict['player_id_2']= match.player_id_2.id if match.player_id_2 else None
					match_dict['tournament_id']= match.tournament_id
					match_dict['tournament_name']= tournament.name
					match_dict['tournament_owner']= tournament.player_id.username if tournament.player_id else None
					match_dict['tournament_start']= tournament.date_start.isoformat() if isinstance(tournament.date_start, datetime) else match.tournament_id.date_start
					match_dict['status']= match.status
					match_dict['match_UUID']= match.match_UUID
					match_dict['tournament_UUID']= match.tournament_UUID
					match_dict['date_time_match']= match.date_time.isoformat() if isinstance(match.date_time, datetime) else match.date_time
					matches_list.append(match_dict)
				except:
					None
			data = json.dumps(matches_list)
			return JsonResponse({'status': 'success', 'message': 'List of matches', 'data': data}, status=200)
	except OperationalError:
		return JsonResponse({'status': 'error', 'message': 'Internal error', 'data': None}, status=500)