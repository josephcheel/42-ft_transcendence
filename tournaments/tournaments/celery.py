# tournamentsapp/celery.py
from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tournaments.settings')

app = Celery('tournaments',brocker='redis://localhost:6379/0')

app.conf.broker_connection_retry_on_startup = True
app.conf.broker_connection_max_retries = 100
app.conf.broker_connection_timeout = 30
app.conf.broker_connection_retry = True

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
#app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
