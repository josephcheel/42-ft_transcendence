import requests
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import json


logger = logging.getLogger('django')
logger.setLevel(logging.DEBUG)


@csrf_exempt
def create_user(request):
    try:
        try:
            data = json.loads(request.body) 
        except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message':'Invalid Json body', 'data' : None}, status=400)
            
        response = requests.post("http://usermanagement:8000/users/create_user/", json=data)
        try:
            response_data = response.json()
            return JsonResponse(response_data, status=response.status_code)
        except ValueError:
            # This shouldn't happen ever, this is just in case I don't return I forget to return a json response
            return JsonResponse({{'status' : 'error', 'data' : None, 'message' : '"Invalid response from usermanagement"'}}, status=500)
    except :
        return JsonResponse({{'status' : 'error', 'data' : None, 'message' : 'Internal error'}}, status=500)
 

@csrf_exempt
def test_logging(request):
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')
    return HttpResponse("Log messages generated.")