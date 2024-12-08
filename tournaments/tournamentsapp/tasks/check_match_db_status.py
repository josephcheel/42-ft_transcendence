# tournamentsapp/tasks.py
from __future__ import absolute_import
from celery import shared_task
from tournamentsapp.models import Matches
from datetime import timedelta
from django.utils import timezone
from tournaments.settings import TIME_DELTA
from tournamentsapp.status_options import StatusMatches
from tournamentsapp.status_options import Rounds
from tournamentsapp.tasks.actualise_tournaments import actualise_tournament
import uuid
import logging

logger = logging.getLogger('django')
@shared_task
def check_match_db_status():
	matches_passed = Matches.objects.filter(date_time = timezone.now() + timedelta(minutes = TIME_DELTA), status = StatusMatches.NOT_PLAYED.value)
	tournament_ids = []
	if len(matches_passed) == 0:
		logger.info('No matches to abort')
		return None
	for mymatch in matches_passed:
		logger.info('Match to aborted: {mymatch.id}')
		mymatch.winner_id = None
		mymatch.looser_id = None
		mymatch.status = StatusMatches.ABORTED.value
		mymatch.save()
		if mymatch.tournament_id not in tournament_ids:
			tournament_ids.append(mymatch.tournament_id)
		actualise_tournament(mymatch.id)
	mymatches = Matches.objects.filter(tournament_id__in=tournament_ids, status__in=[
						StatusMatches.PLAYED.value, StatusMatches.WALKOVER.value])
	while len(mymatches) > 1:
		logger.info("actualizo torneo")
		actualise_tournament(mymatches[0].id)
		mymatches = Matches.objects.filter(tournament_id__in=tournament_ids, status__in=[
				StatusMatches.PLAYED.value, StatusMatches.WALKOVER.value])
	mymatches = Matches.objects.filter(
		tournament_id__in=tournament_ids, 
		status__in=[StatusMatches.PLAYED.value, StatusMatches.WALKOVER.value])
	if len(mymatches) == 1:
		logger.info("one match left without pair")
		match (mymatches[0].round):
			case 1:
				if mymatches[0].round == Rounds.FINAL_ROUND.value and mymatches[0].status == StatusMatches.WALKOVER.value:
					mymatches[0].status = StatusMatches.PLAYED.value
					finish_tournament(tournament.id)
				if mymatches[0].round == Rounds.THIRD_PLACE_ROUND.value and mymatches[0].status == StatusMatches.WALKOVER.value:
					mymatches[0].status = StatusMatches.PLAYED.value
					actualise_tournament(mymatches[0].id)
			case 2:
				actualise_tournament(mymatches[0].id)
			case _:
				new_match = Matches.objects.create()
				for field in mymatches[0]._meta.fields:
					if field.name != "id":  # Skip the ID field to avoid conflicts
						setattr(new_match, field.name, getattr(mymatches[0], field.name))
				new_match.round = Rounds.SEMIFINAL_ROUND.value if new_match.number_round == 3 else Rounds.QUALIFIED_ROUND.value
				new_match.date_time = timezone.now() + timedelta(minutes=TIME_DELTA)
				new_match.number_round -=1
				new_match.save()
				

	return None