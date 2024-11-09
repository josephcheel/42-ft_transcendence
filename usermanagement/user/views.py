from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import OperationalError
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, get_user_model
from user.wrappers import *
import json
import logging
from web3 import Web3


#If testing we dont have usermodel.User so we want to use default

from .models import *
User = get_user_model()

if not settings.DEBUG:
    logger = logging.getLogger('django')
    logger.setLevel(logging.DEBUG)

def transfer_first_founds(user):
	web3 = Web3(Web3.HTTPProvider(settings.GANACHE_URL))
	ganache_url = settings.GANACHE_URL
	web3 = Web3(Web3.HTTPProvider(ganache_url))
	if not web3.is_connected():
		logger.warning("Could not connect to blockchain")
		return False
	new_account = web3.eth.account.create()
	user.ethereum_address = new_account.address
	user.ethereum_private_key = '0x' + new_account._private_key.hex()
	user.save()
	ganache_bank_account = web3.eth.accounts[0]
	tx = {'from': ganache_bank_account,
		  'to': user.ethereum_address,
		  'value': web3.to_wei(10, 'ether'),
		  'gas': 21000,
		  'gasPrice': Web3.to_wei('1', 'gwei'),
		  'nonce': web3.eth.get_transaction_count(ganache_bank_account)}
	signed_tx = web3.eth.account.sign_transaction(
		tx, settings.GANACHE_BANK)
	tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
	web3.eth.wait_for_transaction_receipt(tx_hash)
	return True


def custom_404_view(request, exception=None):
    response_data = {
        'status': 'error',
        'message': 'The requested resource was not found',
        'data': None
    }
    return JsonResponse(response_data, status=404)

@require_post
@validate_creation_fields
@exception_handler
# Need to check email, name, and other infor from front end.
def create_user(request):
    username = request.username #og username in lower case
    password = request.password
    first_name = request.first_name
    last_name = request.last_name
    lowercase_username = request.lowercase_username
    try:
        User.objects.get(lowercase_username=lowercase_username)# need to check email too
        return JsonResponse({'status' : 'error',
                                'message' : "User already Exists",
                                'data' : None},
                                status=409)
    except User.DoesNotExist:
        user = User(username=username,
                    lowercase_username=lowercase_username,
                    tournament_name=username,
                    first_name=first_name,
                    last_name=last_name)
        try:
            user.set_password(password)
            user.save()
            if not transfer_first_founds(user):
                return JsonResponse({'status': 'error',
                                     'message': 'Could not connect to blockchain',
                                     'data': None}, status=500)
        except OperationalError:
            return JsonResponse({'status' : 'error',
                                'message' : 'Internal database error',
                                'data' : None, },
                                status=500)
        return JsonResponse({   'status' : 'success',
                                'message' : 'User created successfully',
                                'data' : None},
                                status=201)

@require_post
@validate_login_credentials
@exception_handler
def login_user(request):
    username = request.username
    password = request.password
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
    
    
@require_post
@exception_handler
def logout_user(request):
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
    

@require_get
@exception_handler
def is_logged_in(request):
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

@require_get
@exception_handler
def list_users(request):
    users = User.objects.all().values('id', 'username')
    return JsonResponse({'status' : 'success', 
                            'data' : list(users), 
                            'message' : 'All registered users'}, 
                            status=200)

# GET current user status or POST new user status (online/offline)


@require_auth
@exception_handler
def user_status(request):
    if request.method == 'GET':    
        username = request.GET.get('username')
        if username is None:
                return JsonResponse({'status': 'error', 'message': 'No username provided', 'data': None}, status=400)
        user_status = UserStatus.objects.get(user=User.objects.get(username=username))
        return JsonResponse({'status' : 'success',
                            'message' : "Retrieved status",
                            'data' : {'is_online' : user_status.is_online}},
                            status=200)     
    elif request.method == 'POST':
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
        return JsonResponse({
                'status': 'error',
                'message': 'Invalid request method, GET or POST required',
                'data': None
            }, status=405)

#Creates a new friendship if it doens't exist


@require_auth
@require_post
@get_friend
@exception_handler
def send_friend_request(request):
    user2 = User.objects.get(username=request.friend)
    if Friendship.are_friends(request.user, user2):
        return JsonResponse({'status' : 'error',
                'message' : "Users are already friends",
                'data' : None}, status=400)
    Friendship.add_friendship(request.user, user2)
    return JsonResponse({'status' : 'success',
            'message' : "Friendship created",
            'data' : None}, status=201)

    
#Changes friendship status, can be use to accept/decline invites or to remove a friendship
@require_auth
@require_post
@get_friend
@get_status
@exception_handler
def change_friendship_status(request):
    status = Friendship.get_status_choice(request.status)
    user2 = User.objects.get(username=request.friend)
    friendship = Friendship.get_friendship(request.user, user2)
    if not friendship.exists():
        return JsonResponse({'status' : 'error',
                            'message' : "Users have no friendship",
                            'data' : None}, status= 404)
    friendship = friendship.first()
    friendship.status = status
    friendship.save()
    return JsonResponse({'status' : 'success',
            'message' : "Friendship modified",
            'data' : None}, status=200)

#Gets all friends


@require_auth
@require_get
@exception_handler
def get_friends(request):
    friends = Friendship.get_friends(request.user)
    return JsonResponse({'status' : 'success',
                'message' : "Got all friends",
                'data' : friends}, status=200)


@require_auth
@require_post
@get_data
@exception_handler
def update_user(request):
    request.user.update_fields(**request.data)
    return JsonResponse({'status' : 'success',
                'message' : "Updated fields",
                'data' : None}, status=200)


@require_auth
@require_post
@exception_handler
def upload_picture(request):
    if 'picture' not in request.FILES:
        logger.info("No picture received in request")
        return JsonResponse({
            'status': 'error',
            'message': 'No picture received',
            'data': {}
        }, status=400)
    picture = request.FILES['picture']
    user_profile_pic= UserProfilePic.objects.get(user=request.user)
    user_profile_pic.update_picture(picture)
    return JsonResponse({'status' : 'success',
                'message' : "Updated profile picture",
                'data' : {
                    'profile_picture_url': request.user.userprofilepic.picture.url
                    }
                }, status=200)


@require_auth
@require_get
@exception_handler
def get_profile_picture_url(request, username):
    user = User.objects.get(username=username)
    profile_pic = UserProfilePic.objects.get(user=user)
    return JsonResponse({'status' : 'success',
                'message' : "Got profile picture",
                'data' : {
                    'profile_picture_url': profile_pic.picture.url
                    }
                }, status=200)


@require_auth
@require_get
@exception_handler
def get_profile(request, username):   
    user = User.objects.get(username=username)
    return JsonResponse({'status' : 'success',
            'message' : "Got user profile",
            'data' : user.get_all(),
            }, status=200)


@require_auth
@require_post
@get_data
@exception_handler
def check_user(request):
    user = User.objects.get(username=request.data.get('username'))
    return JsonResponse({'status': 'success', 'message': 'Checked if users are the same', 'data': {'is_same':user==request.user}}, status=200)
