import requests
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import  ensure_csrf_cookie, csrf_exempt
import logging
import json
from django.conf import settings 
from django.middleware.csrf import get_token

logger = logging.getLogger('django')
logger.setLevel(logging.DEBUG)


def custom_404_view(request, exception=None):
    response_data = {
        'status': 'error',
        'message': 'The requested resource was not found',
        'data': None
    }
    return JsonResponse(response_data, status=404)

@ensure_csrf_cookie
def get_cookie(request):
    return JsonResponse({'status' : 'success', 'data' : None, 'message' : 'You got your cookie now'}, status=200)

@ensure_csrf_cookie
def user(request, subpath):
    response = None
    try:
        if request.method == "POST": 
            try:
                data = json.loads(request.body) 
            except json.JSONDecodeError:
                    return JsonResponse({'status': 'error', 'message':'Invalid Json body', 'data' : None}, status=400)
            response = requests.post(f'http://usermanagement:8000/user/{subpath}/', json=data, cookies=request.COOKIES, headers=request.headers)
        elif request.method == "GET": 
            response = requests.get(f'http://usermanagement:8000/user/{subpath}')
        try:
            response_data = response.json()
            return JsonResponse(response_data, status=response.status_code)
        except ValueError as e:
            # DJANGO Returns HTMLS if in DEBUG Mode, So I am just returning the HTML as DATA
            if settings.DEBUG:
                return HttpResponse(response.text, status=response.status_code, content_type='text/html')
            logger.exception(e)
            return JsonResponse({'status' : 'error', 'data' : None, 'message' : 'Internal error B'}, status=500)
    except Exception as e:
        logger.exception(e)
        return JsonResponse({'status' : 'error', 'data' : None, 'message' : 'Internal error C'}, status=500)
 