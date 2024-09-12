from tournamentsapp.wrappers import validate_credentials, require_post, user_is_authenticated
from django.http import JsonResponse
from tournamentsapp.models import Tournaments, Invitations
from tournamentsapp.status_options import StatusInvitations


try: 
	from usermodel.models import User
except:
	from ..models import User
import math


@require_post
@validate_credentials
def accept_invitation(request):
	data = request.data
	tournament = data.get("tournament_id")
	try:
		tournament = Tournaments.objects.get(id=tournament)
	except Tournaments.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'The tournament does not exist', 'data': None}, status=400)

	player = data.get("username")
	try: 
		player = User.objects.get(username=player)
	except User.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'The user does not exist', 'data': None}, status=400)

	try:
		invitation = Invitations.objects.get(tournament_id=tournament.id, player_id=player.id)
	except Invitations.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'You have not been invited to this tournament', 'data': None}, status=400)
	if player.puntos < tournament.cost:
		return JsonResponse({'status': 'error', 'message': 'You do not have enough points to accept the invitation', 'data': None}, status=400)
	if invitation.status == StatusInvitations.INVITATION_ACCEPTED.value:
		return JsonResponse({'status': 'error', 'message': 'The invitation has already been accepted', 'data': None}, status=400)
	player.puntos_reservados +=tournament.cost
	player.puntos -= tournament.cost
	player.save()
	invitation.status = StatusInvitations.INVITATION_ACCEPTED.value
	invitation.save()
	return JsonResponse({'status': 'success', 'message': 'Invitation accepted successfully', 'data': None}, status=200)
