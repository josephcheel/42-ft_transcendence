# tournamentsapp/tasks.py
from __future__ import absolute_import
from celery import shared_task
from tournamentsapp.models import Matches
from datetime import timedelta
from django.utils import timezone
from tournaments.settings import TIME_DELTA
from tournamentsapp.status_options import StatusMatches
from tournamentsapp.tasks.actualise_tournaments import actualise_tournament


@shared_task
def check_match_db_status():
	print("Running periodic task0")
	# Query the database
	matches = Matches.objects.all()
	print("Running periodic task00")
	print (type(matches))
	print("Running periodic task000")
	if len(matches) == 0:
		return None
	
	print("Running periodic task000")
	# Process the matches (example)
	for match in matches:
		print(f'Match ID: {match.id}, Status: {match.status}')
	matches_passed = Matches.objects.filter(date_time = timezone.now() + timedelta(minutes = TIME_DELTA))
	print("Running periodic task1")
	tournament_ids = []
	print("Running periodic task2")
	if len(matches_passed) == 0:
		return None
	for mymatch in matches_passed:
		# Perform the check or update
		#print(f"Checking record {mymatch.date_time}")
		print("Running periodic task3")
		mymatch.winner_id = None
		mymatch.looser_id = None
		mymatch.status = StatusMatches.PLAYED.value
		mymatch.save()
		print("Running periodic task4")
		if mymatch.tournament_id not in tournament_ids:
			tournament_ids.append(mymatch.tournament_id)
	print("Running periodic task5")
	mymatches = Matches.objects.filter(tournament_id__in=tournament_ids, status__in=[
	                                   StatusMatches.PLAYED.value, StatusMatches.WALKOVER.value])
	while len(mymatches) > 0:
		actualise_tournament.delay(mymatches[0])
		mymatches = Matches.objects.filter(tournament_id__in=tournament_ids, status__in=[
	                                   StatusMatches.PLAYED.value, StatusMatches.WALKOVER.value])


	return None