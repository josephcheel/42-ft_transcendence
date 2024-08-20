from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from django.db import DatabaseError, OperationalError
from django.conf import settings

import json
import logging

if not settings.DEBUG:
    logger = logging.getLogger('django')
    logger.setLevel(logging.DEBUG)

def custom_404_view(request, exception=None):
    response_data = {
        'status': 'error',
        'message': 'The requested resource was not found',
        'data': None
    }
    return JsonResponse(response_data, status=404)


@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) 
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message':'Invalid Json body', 'data' : None}, status=400)
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return JsonResponse({'status': 'error', 'message': 'Empty username or password', 'data' : None}, status=400)
        try:
            user = User.objects.get(username=username)
            return JsonResponse({'status' : 'error', 'message' : "User already Exists", 'data' : None}, status=409)
        except User.DoesNotExist:
            user = User(username=username)
            try:
                user.save_password(password)
            except OperationalError:
                return JsonResponse({'status' : 'error', 'data' : None, 'message' : 'Internal error'}, status=500)
            return JsonResponse({'status' : 'success', 'data' : {'id': user.id, 'username': user.username}, 'message' : 'User created successfully'}, status=201)
        except OperationalError:
            return JsonResponse({'status' : 'error', 'data' : None, 'message' : 'Internal error'}, status=500)
    return JsonResponse({'status' : 'error',  'message': 'Invalid request method', 'data' : None}, status=400)

@csrf_exempt
def list_users(request):
    users = User.objects.all().values('id', 'name', 'password')
    return JsonResponse(list(users), safe=False)