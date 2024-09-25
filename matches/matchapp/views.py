from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import OperationalError
from django.conf import settings
from django.contrib.auth import  get_user_model
from django.core.serializers import serialize
from django.utils import timezone
from .models import Invitation
import json
import logging
from datetime import datetime
#If testing we dont have usermodel.User so we want to use default
try:
    from usermodel.models import User
except:
    pass

User = get_user_model()

if not settings.DEBUG:
    logger = logging.getLogger('django')
    logger.setLevel(logging.DEBUG)

def get_pending_matches(request):
    if request.method == "GET":
        player = request.GET.get('player')
        if not player:
            return JsonResponse({'status': 'error',
                                 'message':'Invalid Json body',
                                 'data' : None},
                                 status=400)
        try:
            try: 
                player = User.objects.get(username=player)
            except User.DoesNotExist:
                return JsonResponse({'status' : 'error',
                                     'message': 'A user does not exist',
                                     'data' : None},
                                     status=404)
            invitations = Invitation.objects.filter(player_id=player, status=2)
            data = serialize('json', invitations)
            data = json.loads(data)
            data = [entry['fields'] for entry in data]
            return JsonResponse({'status': 'success',
                                    'message':'retrived all pending invitations',
                                    'data' : data},
                                    status=200)
        except OperationalError:
                return JsonResponse({'status' : 'error',
                                     'data' : None,
                                     'message' : 'Internal error'},
                                     status=500)
    else:
        return JsonResponse({'status' : 'error',
                            'message': 'Invalid request method',
                            'data' : data},
                            status=400)


def propose_match(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) 
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 
                                 'message':'Invalid Json body', 
                                 'data' : None}, 
                                 status=400)
        start_time = data.get('start_time')
        players = data.get('players')
        if not start_time or not players:
            return JsonResponse({'status': 'error',
                                 'message':'Invalid Json body',
                                 'data' : None},
                                 status=400)
        current_time = datetime.now()
        current_time = timezone.make_aware(current_time, timezone.utc)
        start_time = datetime.fromisoformat(start_time)
        start_time = timezone.make_aware(start_time, timezone.utc)
        if len(players) == 1:
            return JsonResponse({'status': 'error',
                                 'message':'Needs more than one player',
                                 'data' : None},
                                 status=400)  
        for indx, player in enumerate(players):
            try:
                if indx == 0:
                    Invitation.objects.create(
                        creation_time=current_time,
                        start_time=start_time,
                        player_id= User.objects.get(username=player),
                        owner = True,
                        status = 1,
                        )
                else:
                    Invitation.objects.create(
                        creation_time=current_time,
                        start_time=start_time,
                        player_id= User.objects.get(username=player),
                        )
            except User.DoesNotExist:
                return JsonResponse({'status' : 'error',
                                     'message': 'A user does not exist',
                                     'data' : None},
                                     status=404)
            except OperationalError:
                return JsonResponse({'status' : 'error',
                                     'data' : None,
                                     'message' : 'Internal error'},
                                     status=500)
        return JsonResponse({'status' : 'success',
                             'message': 'Sent invitations to all players',
                             'data' : None},
                             status=200)
            
    return JsonResponse({'status' : 'error',
                         'message': 'Invalid request method',
                         'data' : None},
                         status=400)
