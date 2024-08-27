from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import OperationalError
from django.conf import settings
from django.contrib.auth import authenticate, login, get_user_model

#If testing we dont have usermodel.User so we want to use default
try:
    from usermodel.models import User
except:
    pass

User = get_user_model()

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
def is_logged_in(request):
    if request.method == "GET":
        try:
            data = json.loads(request.body) 
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 
                                 'message':'Invalid Json body', 
                                 'data' : None}, 
                                 status=400)
        try:
            user = User.objects.get(username=data.get('username'))
            return JsonResponse({'status': 'success', 
                                 'message':'User is logged in', 
                                 'data' : None}, 
                                 status=200)
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 
                                 'message':'User is not logged in', 
                                 'data' : None}, 
                                 status=404)
        except OperationalError:
            return JsonResponse({'status' : 'error', 
                                 'data' : None, 
                                 'message' : 'Internal error'}, 
                                 status=500)
    else:
        return JsonResponse({'status' : 'error',  
                             'message': 'Invalid request method', 
                             'data' : None}, 
                             status=400)



@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body) 
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error',
                                 'message':'Invalid Json body',
                                 'data' : None}, 
                                 status=400)
        user = authenticate(request, username=data.get('username'), password=data.get('password'))
        try:
            if user is not None:
                login(request, user)
                return JsonResponse({'status' : 'success',
                                    'message': 'user is loged in',
                                    'data' : None},
                                    status=200)
            else:
                return JsonResponse({'status' : 'error',
                                     'message': 'Invalid credentials',
                                     'data' : None},
                                     status=401)
        except OperationalError:
            return JsonResponse({'status' : 'error',
                                 'message' : 'Internal error',
                                  'data' : None,}, 
                                  status=500)            
    return JsonResponse({'status' : 'error',
                         'message': 'Invalid request method',
                         'data' : None},
                         status=400)


@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) 
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error',
                                 'message':'Invalid Json body',
                                 'data' : None},
                                 status=400)
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return JsonResponse({'status': 'error',
                                 'message': 'Empty username or password',
                                 'data' : None},
                                 status=400)
        try:
            user = User.objects.get(username=username)
            return JsonResponse({'status' : 'error',
                                 'message' : "User already Exists",
                                 'data' : None},
                                 status=409)
        except User.DoesNotExist:
            user = User(username=username)
            try:
                user.set_password(password)
                user.save()
            except OperationalError:
                return JsonResponse({'status' : 'error',
                                    'message' : 'Internal error',
                                    'data' : None, },
                                    status=500)
            return JsonResponse({'status' : 'success',
                                 'message' : 'User created successfully',
                                 'data' : {'id': user.id, 'username': user.username}},
                                 status=201)
        except OperationalError:
            return JsonResponse({'status' : 'error',
                                'message' : 'Internal error',
                                'data' : None},
                                status=500)
    return JsonResponse({'status' : 'error',
                         'message': 'Invalid request method',
                         'data' : None},
                         status=400)

@csrf_exempt
def list_users(request):
    users = User.objects.all().values('id', 'name', 'password')
    return JsonResponse(list(users), safe=False)