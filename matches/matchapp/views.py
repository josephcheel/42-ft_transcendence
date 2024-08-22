from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import OperationalError
from django.conf import settings
from django.contrib.auth import  get_user_model

#If testing we dont have usermodel.User so we want to use default
try:
    from usermodel.models import User
except:
    pass
from .models import Invitation

User = get_user_model()

import json
import logging
from datetime import datetime

# Create your views here.
if not settings.DEBUG:
    logger = logging.getLogger('django')
    logger.setLevel(logging.DEBUG)

@csrf_exempt
def propose_match(request):
    if request.method == 'POST':
        current_time = datetime.now()
        data = json.loads(request.body) 
        start_time = data.get('start_time')
        start_time = datetime.fromisoformat(start_time)
        players = data.get('players')
        if not start_time or not players:
            return JsonResponse({'status': 'error', 'message':'Invalid Json body', 'data' : None}, status=400)
        for indx, player in enumerate(players):
            try:
                if indx == 0:
                    Invitation.objects.create(
                        creation_time=current_time,
                        start_time=start_time,
                        player_id=User.objects.get(username=player),
                        owner = True,
                        status =1,
                        )
                else:
                    Invitation.objects.create(
                        creation_time=current_time,
                        start_time=start_time,
                        player_id=User.objects.get(username=player),
                        )
            except User.DoesNotExist:
                return JsonResponse({'status' : 'error',  'message': 'A user does not exist', 'data' : None}, status=404)
            except OperationalError:
                return JsonResponse({'status' : 'error', 'data' : None, 'message' : 'Internal error 1'}, status=500)
            except:
                return JsonResponse({'status' : 'error', 'data' : None, 'message' : 'Internal error 2'}, status=500)
 
        return JsonResponse({'status' : 'success',  'message': 'Sent invitations to all players', 'data' : None}, status=200)
            
    return JsonResponse({'status' : 'error',  'message': 'Invalid request method', 'data' : None}, status=400)
