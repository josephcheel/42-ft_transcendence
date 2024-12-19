# tournamentsapp/tasks.py
from __future__ import absolute_import
from celery import shared_task
from tournamentsapp.models import Matches, Tournaments
from datetime import timedelta
from django.utils import timezone
from tournaments.settings import TIME_DELTA
from tournamentsapp.status_options import StatusMatches, StatusTournaments
from tournamentsapp.tasks.actualise_tournaments import actualise_tournament
from tournamentsapp.tasks.check_round_tournament import check_round_tournament
import uuid
import logging

logger = logging.getLogger('django')
@shared_task
def check_match_db_status():
	matches_passed = Matches.objects.filter(
		date_time__lt=timezone.now() - timedelta(minutes=TIME_DELTA),
		status=StatusMatches.WAITING_PLAYER1.value
	)
	if matches_passed.count() > 0:
		for mymatch in matches_passed:
			mymatch.winner_id = mymatch.player_id_2
			mymatch.looser_id = mymatch.player_id_1
			mymatch.points_looser = 0
			mymatch.status = StatusMatches.PLAYED.value
			mymatch.save()
			if check_round_tournament(mymatch.tournament_id):
				actualise_tournament(mymatch.tournament_id)
	matches_passed = Matches.objects.filter(
		date_time__lt=timezone.now() - timedelta(minutes=TIME_DELTA),
		status=StatusMatches.WAITING_PLAYER2.value
	)
	if matches_passed.count() > 0:
		for mymatch in matches_passed:
			mymatch.winner_id = mymatch.player_id_1
			mymatch.looser_id = mymatch.player_id_2
			mymatch.points_looser = 0
			mymatch.status = StatusMatches.PLAYED.value
			mymatch.save()
			if check_round_tournament(mymatch.tournament_id):
				actualise_tournament(mymatch.tournament_id)
	matches_passed = Matches.objects.filter(
    	date_time__lt=timezone.now() - timedelta(minutes=TIME_DELTA),
		status=StatusMatches.NOT_PLAYED.value
	)
	logger.debug(f'Time Zone now: {timezone.now()}, time zone now + delta time: {timezone.now() + timedelta(minutes = TIME_DELTA)}')
	tournament_ids = []
	if matches_passed.count() == 0:
		logger.debug('No matches to abort')
		return None
	for mymatch in matches_passed:
		logger.debug(f'Time Zone now: {timezone.now()}, time zone now + delta time: {timezone.now() + timedelta(minutes = TIME_DELTA)}, matches passed: {mymatch.date_time}')
		mymatch.winner_id = None
		mymatch.looser_id = None
		mymatch.status = StatusMatches.ABORTED.value
		mymatch.save()
		if mymatch.tournament_id not in tournament_ids:
			tournament_ids.append(mymatch.tournament_id)
	for mytournament_id in tournament_ids:
		if check_round_tournament(mytournament_id):
			actualise_tournament(mytournament_id)
