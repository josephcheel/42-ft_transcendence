from django.dispatch import receiver
from .metrics import * 
import logging
from asgiref.sync import async_to_sync



from django.dispatch import Signal

user_connected = Signal()
user_disconnected = Signal()

logger = logging.getLogger('django')
logger.setLevel(logging.DEBUG)

@receiver(user_connected)
def increment_connections(sender, request, **kwargs):
    logger.info("I am inside signals")
    connections_counter.inc()

@receiver(user_disconnected)
def decrement_connections(sender, request, **kwargs):
    connections_counter.dec()