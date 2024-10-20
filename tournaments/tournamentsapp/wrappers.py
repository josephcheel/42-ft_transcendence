
from django.http import JsonResponse
import json
from functools import wraps

def user_is_authenticated(function):
	@wraps(function)
	def wrapper(request, *args, **kwargs):
		if not request.user.is_authenticated:
			return JsonResponse({'status': 'error',
								'message': 'User not authenticated',
								'data': None},
							   status=401)

		return function(request, *args, **kwargs)
	return wrapper

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

def validate_credentials(func):
	@wraps(func)
	def wrapper(request, *args, **kwargs):
		try:
			request.data = json.loads(request.body)
		except json.JSONDecodeError:
			return JsonResponse({'status': 'error', 'message': 'Invalid JSON body', 'data': None}, status=400)

		request.username = request.data.get('username')
		request.password = request.data.get('password')

		if not request.username or not request.password:
			return JsonResponse({'status': 'error', 'message': 'Empty username or password', 'data': None}, status=400)
		request.username = request.username.lower()
		return func(request, *args, **kwargs)
	return wrapper

def validate_json(func):
	@wraps(func)
	def wrapper(request, *args, **kwargs):
		try:
			request.data = json.loads(request.body)
		except json.JSONDecodeError:
			return JsonResponse({'status': 'error', 'message': 'Invalid JSON body', 'data': None}, status=400)

		return func(request, *args, **kwargs)
	return wrapper
