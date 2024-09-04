from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import OperationalError
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, get_user_model
from .wrappers import validate_credentials, require_post, require_get, get_friend
import json
import logging

#If testing we dont have usermodel.User so we want to use default

from .models import UserStatus, Friendship
User = get_user_model()



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

             
@require_post
@validate_credentials
def create_user(request):
    username = request.username #og username in lower case
    password = request.password
    original_username = request.original_username
    try:
        User.objects.get(username=username)# need to check email too
        return JsonResponse({'status' : 'error',
                                'message' : "User already Exists",
                                'data' : None},
                                status=409)
    except User.DoesNotExist:
        user = User(username=username, original_username=original_username)
        try:
            user.set_password(password)
            user.save()
            UserStatus.objects.get_or_create(user=user)
        except OperationalError:
            return JsonResponse({'status' : 'error',
                                'message' : 'Internal database error',
                                'data' : None, },
                                status=500)
        return JsonResponse({'status' : 'success',
                                'message' : 'User created successfully',
                                'data' : {'id': user.id, 'username': user.original_username}},
                                status=201)
    except OperationalError:
        return JsonResponse({'status' : 'error',
                            'message' : 'Internal database error',
                            'data' : None},
                            status=500)
    except Exception as e:
        logger.error(e)
        return JsonResponse({'status': 'error',
                                'message': 'Internal server error',
                                'data': None},
                                status=500)  
    


@require_post
@validate_credentials
def login_user(request):
    username = request.original_username
    password = request.password
    try:
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_status= UserStatus.objects.get(user=user)
            user_status.change_status(True) 
            return JsonResponse({'status' : 'success',
                                'message': 'user is logged in',
                                'data' : None},
                                status=200)
        else:
            return JsonResponse({'status' : 'error',
                                    'message': 'Invalid credentials',
                                    'data' : None},
                                    status=401)
    except OperationalError:
        return JsonResponse({'status' : 'error',
                                'message' : 'Internal database error',
                                'data' : None,}, 
                                status=500)
    except Exception as e:
        logger.error(e)
        return JsonResponse({'status': 'error',
                                'message': 'Internal server error',
                                'data': None},
                                status=500)
    
@require_post
def logout_user(request):
    try:
        if request.user.is_authenticated:
            user_status = UserStatus.objects.get(user=request.user)
            logout(request)
            user_status.change_status(False) 
            return JsonResponse({'status' : 'success',
                                'message': 'user has been logged out',
                                'data' : None},
                                status=200)        
        else:
            return JsonResponse({'status' : 'error',
                                    'message': 'Forbidden',
                                    'data' : None},
                                    status=403)
    except OperationalError:
        return JsonResponse({'status' : 'error',
                                'message' : 'Internal database error',
                                'data' : None,}, 
                                status=500)
    except Exception as e:
        logger.error(e)
        return JsonResponse({'status': 'error',
                                'message': 'Internal server error',
                                'data': None},
                                status=500)
    

@require_get
def is_logged_in(request):
    try:
        if request.user.is_authenticated:
            return JsonResponse({'status': 'success', 
                                'message':'User is logged in', 
                                'data' : None}, 
                                status=200)
        else:
            return JsonResponse({'status': 'error', 
                                'message':'Unauthorized', 
                                'data' : None}, 
                                status=401)
    except OperationalError:
        return JsonResponse({'status' : 'error', 
                                'data' : None, 
                                'message' : 'Internal database error'}, 
                                status=500)
    except Exception as e:
        logger.error(e)
        return JsonResponse({'status': 'error',
                                'message': 'Internal server error',
                                'data': None},
                                status=500)

@require_get
def list_users(request):
    try:
        users = User.objects.all().values('id', 'username')
        return JsonResponse({'status' : 'success', 
                                'data' : list(users), 
                                'message' : 'All registered users'}, 
                                status=200)
    except OperationalError:
        return JsonResponse({'status' : 'error', 
                        'data' : None, 
                        'message' : 'Internal database error'}, 
                        status=500)
    except Exception as e:
        logger.error(e)
        return JsonResponse({'status': 'error',
                                'message': 'Internal server error',
                                'data': None},
                                status=500)


def user_status(request):
    if request.method == 'GET':    
        username = request.GET.get('username')
        if username is None:
                return JsonResponse({'status': 'error', 'message': 'No username provided', 'data': None}, status=400)
        try:
            user_status = UserStatus.objects.get(user=User.objects.get(username=username))
            return JsonResponse({'status' : 'success',
                                'message' : "Retrieved status",
                                'data' : {'is_online' : user_status.is_online}},
                                status=200)     

        except User.DoesNotExist:
            return JsonResponse({'status' : 'error',
                                'message' : "User does not exists",
                                'data' : None},
                                status=404)
        except OperationalError:
            return JsonResponse({'status' : 'error', 
                            'data' : None, 
                            'message' : 'Internal database error'}, 
                            status=500)
        except Exception as e:
            logger.error(e)
            return JsonResponse({'status': 'error',
                                    'message': 'Internal server error',
                                    'data': None},
                                    status=500)
    elif request.method == 'POST':
        try:
            if request.user.is_authenticated:
                try:
                    request.data = json.loads(request.body)
                except json.JSONDecodeError:
                    return JsonResponse({'status': 'error',
                                         'message': 'Invalid JSON body',
                                         'data': None},
                                         status=400)
                status = request.data.get('status')
                if  status not in ['online', 'offline']:
                    return JsonResponse({'status': 'error',
                                         'message': 'Invalid JSON body',
                                         'data': None},
                                         status=400)
                status = True if status == 'online' else False
                UserStatus.objects.get(user=request.user).change_status(status)
                return JsonResponse({'status': 'success',
                                     'message': 'Updated status',
                                     'data': None},
                                     status=200)
            else:
                return JsonResponse({'status': 'error',
                                     'message': 'No valid user in request',
                                     'data': None}, status=400)
        except OperationalError:
            return JsonResponse({'status' : 'error', 
                            'data' : None, 
                            'message' : 'Internal database error'}, 
                            status=500)            
        except Exception as e:
            logger.error(e)
            return JsonResponse({'status': 'error',
                                    'message': 'Internal server error',
                                    'data': None},
                                    status=500)
    else:
        return JsonResponse({
                'status': 'error',
                'message': 'Invalid request method, GET or POST required',
                'data': None
            }, status=405)
        
@require_post
@get_friend
def send_friend_request(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status' : 'error',
                            'message': 'Invalid credentials',
                            'data' : None},
                            status=401)
    try:

        user2 = User.objects.get(username=request.friend)
        if Friendship.are_friends(request.user, user2):
            return JsonResponse({'status' : 'error',
                    'message' : "Users are already friends",
                    'data' : None}, status=400)
        Friendship.add_friendship(request.user, user2)
        return JsonResponse({'status' : 'success',
                'message' : "Friendship created",
                'data' : None}, status=201)
    except User.DoesNotExist:
        return JsonResponse({'status' : 'error',
                            'message' : "User does not exists",
                            'data' : None}, status=404)
    except OperationalError:
        return JsonResponse({'status' : 'error', 
                        'data' : None, 
                        'message' : 'Internal database error'}, 
                        status=500)
    except Exception as e:
        logger.error(e)
        return JsonResponse({'status': 'error',
                                'message': 'Internal server error',
                                'data': None},
                                status=500)
