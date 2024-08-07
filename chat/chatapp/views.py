from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Chatsession
from django.db import DatabaseError, OperationalError
from django.conf import settings

import json
import logging

if not settings.DEBUG:
    logger = logging.getLogger('django')
    logger.setLevel(logging.DEBUG)


def send_message(request):
    pass