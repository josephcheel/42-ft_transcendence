
from django.http import JsonResponse
import json
from functools import wraps
from django.db import OperationalError
import logging
from django.conf import settings
from django.contrib.auth import get_user_model 

User = get_user_model()

if not settings.DEBUG:
    logger = logging.getLogger('django')
    logger.setLevel(logging.DEBUG)

def require_get(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.method != "GET":
            return JsonResponse({'status' : 'error',  
                             'message': 'Invalid request method, GET required', 
                             'data' : None}, 
                             status=405)
        return func(request, *args, **kwargs)
    return wrapper

def require_post(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.method != "POST":
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid request method, POST required',
                'data': None
            }, status=405)
        return func(request, *args, **kwargs)
    return wrapper

def validate_creation_fields(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            request.data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON body', 'data': None}, status=400)
        request.username = request.data.get('username')
        request.password = request.data.get('password')
        request.first_name = request.data.get('first_name')
        request.last_name = request.data.get('last_name')

        if not request.username or not request.password or not request.first_name or not request.last_name:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields', 'data': None}, status=400)
        request.lowercase_username = request.username.lower()
        return func(request, *args, **kwargs)
    return wrapper


def validate_login_credentials(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            request.data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON body', 'data': None}, status=400)
        request.username = request.data.get('username')
        request.password = request.data.get('password')

        if not request.username or not request.password:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields', 'data': None}, status=400)
        request.lowercase_username = request.data.get('username').lower()
        logger.info(request.username)
        return func(request, *args, **kwargs)
    return wrapper



def get_friend(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            request.data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON body', 'data': None}, status=400)
        request.friend = request.data.get('username')

        if not request.friend:
            return JsonResponse({'status': 'error', 'message': 'Empty username', 'data': None}, status=400)
        request.friend = request.friend.lower()
        return func(request, *args, **kwargs)
    return wrapper

def get_status(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            request.data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON body', 'data': None}, status=400)
        request.status = request.data.get('status')

        if request.status not in ["accepted","declined"]:
            return JsonResponse({'status': 'error', 'message': 'Invalid status', 'data': None}, status=400)
        return func(request, *args, **kwargs)
    return wrapper


def require_auth(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'status' : 'error',
                                'message': 'Invalid credentials',
                                'data' : None},
                                status=401)
        return func(request, *args, **kwargs)
    return wrapper


def exception_handler(view_func):
    def wrapper(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except User.DoesNotExist:
            return JsonResponse({'status' : 'error',
                            'message' : "User does not exists",
                            'data' : None},
                            status=404)
        except OperationalError:
            return JsonResponse({
                'status': 'error',
                'data': None,
                'message': 'Internal database error'
            }, status=500)
        except Exception as e:
            logger.error(e)
            return JsonResponse({
                'status': 'error',
                'message': 'Internal server error',
                'data': None
            }, status=500)
    return wrapper

def get_data(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            request.data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON body', 'data': None}, status=400)
        if not request.data:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON body', 'data': None}, status=400)
        return func(request, *args, **kwargs)
    return wrapper