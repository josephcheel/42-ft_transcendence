# tournamentsapp/tasks.py
from celery import shared_task
from tournamentsapp.models import Matches
from datetime import timedelta
from django.utils import timezone
from tournaments.settings import TIME_DELTA

@shared_task
def check_database_status():
#    matches_passed = Matches.objects.filter(date_time = timezone.now() + timedelta(minutes = TIME_DELTA))
#    for record in matches_passed:
        # Perform the check or update
#        print(f"Checking record {record.date_time}")
    print("Running periodic task")
    return None