from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Chatsession
from django.db import DatabaseError, OperationalError
from django.conf import settings
import requests
import json
import logging

if not settings.DEBUG:
    logger = logging.getLogger('django')
    logger.setLevel(logging.DEBUG)


def send_message(request):
    pass

@csrf_exempt
def test_check(request):
    response = None
    try:
        try:
            data = json.loads(request.body) 
        except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message':'Invalid Json body', 'data' : None}, status=400)
        response = requests.post(f'http://usermanagement:8000/users/is_logged_in/', json=data)
        try:
            response_data = response.json()
            return JsonResponse(response_data, status=response.status_code)
        except ValueError:
            # DJANGO Returns HTMLS if in DEBUG Mode, So I am just returning the HTML as DATA
            if settings.DEBUG:
                return HttpResponse(response.text, status=response.status_code, content_type='text/html')
            return JsonResponse({'status' : 'error', 'data' : None, 'message' : 'Internal error B'}, status=500)
    except:
        return JsonResponse({'status' : 'error', 'data' : None, 'message' : 'Internal error C'}, status=500)