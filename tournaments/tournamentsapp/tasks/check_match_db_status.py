# tournamentsapp/tasks.py
from celery import shared_task
from tournamentsapp.models import Matches
from datetime import timedelta
from django.utils import timezone
from tournaments.settings import TIME_DELTA
from tournamentsapp.status_options import StatusMatches
from tournamentsapp.tasks.actualise_tournaments import actualise_tournament

@shared_task
def check_match_db_status():
	print("Running periodic task")
	matches_passed = Matches.objects.filter(date_time = timezone.now() + timedelta(minutes = TIME_DELTA))
	tournament_ids = []
	for mymatch in matches_passed:
		# Perform the check or update
		print(f"Checking record {mymatch.date_time}")
		mymatch.winne_id = None
		mymatch.looser_id = None
		mymatch.status = StatusMatches.PLAYED.value
		mymatch.save()
		if mymatch.tournament_id not in tournament_ids:
			tournament_ids.append(mymatch.tournament_id)
	mymatches = Matches.objects.filter(tournament_id__in=tournament_ids, status__in=[StatusMatches.PLAYED.value, StatusMatches.WALKOVER.value])
	while len(mymatches) > 0:
		actualise_tournament(mymatches[0])
		mymatches = Matches.objects.filter(tournament_id__in=tournament_ids, status__in=[
	                                   StatusMatches.PLAYED.value, StatusMatches.WALKOVER.value])


	return None