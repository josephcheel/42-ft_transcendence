from tournamentsapp.wrappers import require_get, exception_handler, validate_credentials
from tournamentsapp.models import Invitations
from datetime import datetime
from django.db import OperationalError
from django.http import JsonResponse
import json

from user.models import User

@require_get
@exception_handler
#@validate_credentials
def list_invitations(request,username):
	#player = username
	try:
		# try:
		# player = User.objects.get(username=player)
		# except User.DoesNotExist:
		# return JsonResponse({'status': 'error', 'message': 'A user does not exist', 'data': None}, status=404)
		player = User.objects.get(username=username)
		invitation_data = Invitations.objects.filter(player_id=player.id)
		# Convert any datetime fields to string
		invitation_list = list(invitation_data.values())
		for invitation in invitation_list:
			for key, value in invitation.items():
				if isinstance(value, datetime):
					invitation[key] = value.isoformat()
		data = json.dumps(invitation_list)
		return JsonResponse({'status': 'success', 'message': 'List of invitations cereated', 'data': data}, status=200)
	except OperationalError:
		return JsonResponse({'status': 'error', 'message': 'Internal error', 'data': None}, status=500)
