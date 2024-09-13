from tournamentsapp.wrappers import validate_credentials, require_get, user_is_authenticated
from django.http import JsonResponse
from tournamentsapp.models import Tournaments

try:
	from usermodel.models import User
except:
	from tournamentsapp.models import User
import math


@require_get
@validate_credentials
#@user_is_authenticated
def edit_tournament(request):
	data = request.data
	user = User.objects.get(username = data("user"))
	
	tournament_id = data("tournament_id")
	try:
		tournament = Tournaments.object.get(user_id = User.id, id = tournament_id).values()
	except:
		return JsonResponse({'status': 'error', 'message': 'The tournament does not exist', 'data': None}, status=404)
	return JsonResponse(list(tournament), safe= False)
