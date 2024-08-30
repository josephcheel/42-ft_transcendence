from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .wrappers import validate_credentials, require_post, require_get
from django.contrib.auth import get_user_model
from django.http import JsonResponse
import json
try: 
    from usermodel.models import User
except:
    pass

User = get_user_model()

# Create your views here.
def custom_404_view(request, exception=None):
    response_data = {
        'status': 'error',
        'message': 'The requested resource was not found',
        'data': None
    }
    return JsonResponse(response_data, status=404)

@csrf_exempt
@require_post
@validate_credentials
def create_tournements(request):
    username = request.username
    try:
        data = json.loads(request.body) 
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 
                                'message':'Invalid Json body', 
                                'data' : None}, 
                                status=400)    
    tournements = Tournements.objects.all()
    tournements_list = []
    for tournement in tournements:
        tournements_list.append({
            'name': tournement.name,
            'Date': tournement.Date,
            'max_players': tournement.max_players,
            'price_1': tournement.price_1,
            'price_2': tournement.price_2,
            'price_3': tournement.price_3,
            'winner': tournement.winner,
            'second': tournement.second,
            'third': tournement.third,
            'hashprevius': tournement.hashprevius,
            'hash': tournement.hash
        })
        return JsonResponse({'status': 'success', 'message': 'Tournements fetched successfully', 'data': tournements_list}, status=200)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method', 'data': None}, status=400)