from tournamentsapp.wrappers import require_post, validate_json, user_is_authenticated
import json
from django.http import JsonResponse
from tournamentsapp.status_options import StatusMatches
from tournamentsapp.models import Matches
from datetime import timedelta
from django.utils import timezone
try: 
	from usermodel.models import User
except:
	from tournamentsapp.models import User

@require_post
@user_is_authenticated
@validate_json
def start_match(request):
	data = request.data
	player = request.user
	match_id = data.get('UUID')
	try:
		mymatch = Matches.objects.get(match_UUID=match_id)
	except Matches.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'A match does not exist', 'data': None}, status=400)
	if mymatch.date_time > timezone.now()- timedelta(minutes=1):
		return JsonResponse({'status': 'error', 'message': 'the match can only start 1 minute before', 'data': None}, status=400)
	if mymatch.player_id_1.id != player.id and mymatch.player_id_2.id != player.id: 
		return JsonResponse({'status': 'error', 'message': 'You are not a player of this match', 'data': None}, status=400)
	if mymatch.status == StatusMatches.PLAYED.value:
		return JsonResponse({'status': 'error', 'message': 'The match has already been played', 'data': None}, status=400)
	match player.id:
		case mymatch.player_id_1.id:
			mymatch.is_player1_in_room = True
			if mymatch.is_player2_in_room:
				mymatch.status = StatusMatches.STARTED.value
				the_message = 'Match started successfully'
			else:
				the_message = 'Waiting for player 2 to start the match'
				mymatch.status = StatusMatches.WAITING_PLAYER2.value
		case mymatch.player_id_2.id:
			mymatch.is_player2_in_room = True
			if mymatch.is_player1_in_room:
				mymatch.status = StatusMatches.STARTED.value
				the_message = 'Match started successfully'
			else:
				mymatch.status = StatusMatches.WAITING_PLAYER1.value
				the_message = 'Waiting for player 1 to start the match'
	data = json.dumps({'status': mymatch.status})
	mymatch.save()
	return JsonResponse({'status': 'success', 'message': the_message, 'data': data}, status=200)
