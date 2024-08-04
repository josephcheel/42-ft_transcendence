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
            name = data.get('name')
            password = data.get('password')
            user = User.objects.create(name=name, password=password)
            return JsonResponse({'id': user.id, 'name': user.name, 'password': user.password}, status=201)
        except:
            return JsonResponse({'error': 'Error processing request'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def list_users(request):
    users = User.objects.all().values('id', 'name', 'password')
    return JsonResponse(list(users), safe=False)