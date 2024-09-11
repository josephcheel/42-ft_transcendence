from tournamentsapp.wrappers import require_get, user_is_authenticated
from tournamentsapp.models import Tournaments
from datetime import datetime
from django.core.serializers import serialize
import json
try:
	User = get_user_model()
except:
	from tournamentsapp.models import User

@require_get
@user_is_authenticated
def list_tournaments(request):
	player = request.user.username
	try:
		# try:
		# player = User.objects.get(username=player)
		# except User.DoesNotExist:
		# return JsonResponse({'status': 'error', 'message': 'A user does not exist', 'data': None}, status=404)
		player = User.objects.get(username=request.username)
		print ('---------------------------------------------------')
		print('player', player)
		print('---------------------------------------------------')
		tournaments = Tournaments.objects.filter(player_id=player.id)
		# Convert any datetime fields to string
		tournament_list = list(tournament_data.values())
		for tournament in tournament_list:
			for key, value in tournament.items():
				if isinstance(value, datetime):
					tournament[key] = value.isoformat()

		data = json.dumps(tournament_list)
		return JsonResponse({'status': 'success', 'message': 'List of tournaments cereated', 'data': data}, status=200)
	except OperationalError:
		return JsonResponse({'status': 'error', 'message': 'Internal error', 'data': None}, status=500)
