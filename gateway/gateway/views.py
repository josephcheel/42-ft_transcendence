import requests
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import  ensure_csrf_cookie, csrf_exempt
import logging
import json
from django.conf import settings 
import os

home_directory = os.path.expanduser('~')
logger = logging.getLogger('django')
logger.setLevel(logging.DEBUG)

def custom_404_view(request, exception=None):
    response_data = {
        'status': 'error',
        'message': 'The requested resource was not found',
        'data': None
    }
    return JsonResponse(response_data, status=404)

def handle_request(request, internal_url, subpath):
    response = None
    try:
        if request.method == 'POST' and request.FILES:
            form_data = request.POST
            files = {'picture': request.FILES['picture']}
            headers = dict(request.headers)
            headers.pop('Content-Type', None)
            response = requests.post(
                f'http://{internal_url}{subpath}/',
                data=form_data, 
                files=files, 
                cookies=request.COOKIES, 
                headers=headers
            )
        elif request.method == "POST": 
            try:
                data = json.loads(request.body)
                response = requests.post(f'http://{internal_url}{subpath}/', json=data, cookies=request.COOKIES, headers=request.headers, timeout=10)
            except json.JSONDecodeError:
                response = requests.post(f'http://{internal_url}{subpath}/', cookies=request.COOKIES, headers=request.headers, timeout=10)
        elif request.method == "GET": 
            response = requests.get(f'http://{internal_url}{subpath}', cookies=request.COOKIES, headers=request.headers, timeout=10)
        try:
            response_data = response.json()
            #ensure Set cookies headers are properly set
            gateway_response = JsonResponse(response_data, status=response.status_code)
            for cookie in response.raw.headers.getlist('Set-Cookie'):
                gateway_response['Set-Cookie'] = cookie
            return gateway_response
        except ValueError as e:
            # DJANGO Returns HTMLS if in DEBUG Mode, So I am just returning the HTML as DATA
            if settings.DEBUG:
                return HttpResponse(response.text, status=response.status_code, content_type='text/html')
            logger.exception(e)
            return JsonResponse({'status' : 'error', 'data' : None, 'message' : 'Internal error 1'}, status=500)
    except Exception as e:
        logger.exception(e)
        return JsonResponse({'status' : 'error', 'data' : None, 'message' : 'Internal error 2'}, status=500)

@ensure_csrf_cookie
def tournaments(request, subpath):
    return handle_request(request, "tournaments:8000/tournaments/", subpath)

@ensure_csrf_cookie
def user(request, subpath):
    return handle_request(request, "usermanagement:8000/user/", subpath)

@ensure_csrf_cookie
def get_cookie(request):
    return JsonResponse({'status' : 'success', 'data' : None, 'message' : 'You got your cookie now'}, status=200)

