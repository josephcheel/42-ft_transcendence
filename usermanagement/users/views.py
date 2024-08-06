from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
import json


@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) 
            username = data.get('username')
            password = data.get('password')
            if not username or not password:
                return JsonResponse({'error': 'Empty username or password'}, status=400)
            try:
                user = User.objects.get(username=username)
                return JsonResponse({'error': "User already Exists"}, status=409)
            except User.DoesNotExist:
                user = User(username=username)
                user.save_password(password)
                return JsonResponse({'id': user.id, 'name': user.username}, status=201)
        except:
            return JsonResponse({'error': 'Error processing request'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def list_users(request):
    users = User.objects.all().values('id', 'name', 'password')
    return JsonResponse(list(users), safe=False)