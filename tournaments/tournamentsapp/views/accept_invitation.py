from tournamentsapp.wrappers import require_post, user_is_authenticated, validate_json
from django.http import JsonResponse
from tournamentsapp.models import Tournaments, Invitations
from tournamentsapp.status_options import StatusInvitations


from user.models import User


@require_post
@user_is_authenticated
@validate_json
def accept_invitation(request):
	data = request.data
	tournament = data.get("tournament_id")
	status = data.get("status")
	try:
		tournament = Tournaments.objects.get(id=tournament)
	except Tournaments.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'The tournament does not exist', 'data': None}, status=400)

	player = request.user
#	try: 
#		player = User.objects.get(username=player)
#	except User.DoesNotExist:
#		return JsonResponse({'status': 'error', 'message': 'The user does not exist', 'data': None}, status=400)

	try:
		invitation = Invitations.objects.get(tournament_id=tournament.id, player_id=player.id)
	except Invitations.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'You have not been invited to this tournament', 'data': None}, status=400)
	if player.puntos < tournament.cost:
		return JsonResponse({'status': 'error', 'message': 'You do not have enough points to accept the invitation', 'data': None}, status=400)
	if not status:
		invitation.status = StatusInvitations.INVITATION_REFUSED.value
		invitation.save()
		return JsonResponse({'status': 'success', 'message': 'The invitation has already been refused', 'data': None}, status=200)
	player.puntos_reservados +=tournament.cost
	player.puntos -= tournament.cost
	player.save()
	invitation.status = StatusInvitations.INVITATION_ACCEPTED.value
	invitation.save()
	return JsonResponse({'status': 'success', 'message': 'Invitation accepted successfully', 'data': None}, status=200)
