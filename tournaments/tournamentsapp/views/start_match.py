from tournamentsapp.wrappers import require_post
import json
from django.http import JsonResponse
from tournamentsapp.status_options import StatusMatches
from tournamentsapp.models import Matches

try: 
	from usermodel.models import User
except:
	from tournamentsapp.models import User

@require_post
def start_match(request):
	request.data = json.loads(request.body)
	try:
		request.data = json.loads(request.body)
	except json.JSONDecodeError:
		return JsonResponse({'status': 'error', 'message': 'Invalid JSON body', 'data': None}, status=400)
	data = request.data
	player = data.get('player')
	try:
		player = User.objects.get(username=player)
	except User.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'A user does not exist', 'data': None}, status=404)
	match_id = data.get('match_id')
	try:
		match = Matches.objects.get(id=match_id)
	except Matches.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'A match does not exist', 'data': None}, status=404)
	if match.player_id_1 != player.id and match.player_id_2 != player.id:
		return JsonResponse({'status': 'error', 'message': 'You are not a player of this match', 'data': None}, status=403)
	if match.status == StatusMatches.PLAYED.value:
		return JsonResponse({'status': 'error', 'message': 'The match has already been played', 'data': None}, status=400)
	match.status = StatusMatches.STARTED.value
	match.save()
	return JsonResponse({'status': 'success', 'message': 'Match started successfully', 'data': None}, status=200)
