from __future__ import absolute_import, unicode_literals
from tournamentsapp.status_options import StatusTournaments, Rounds
from tournamentsapp.models import Tournaments, Matches
from celery import shared_task

try: 
	from user.models import User
except:
	from tournamentsapp.models import User

@shared_task
def finish_tournament(tournament_id):
	tournament = Tournaments.objects.get(id=tournament_id)
	list_of_matches = Matches.objects.filter(tournament_id=tournament.id)
	for match in list_of_matches:
		if match.round == Rounds.FINAL_ROUND.value:
			if match.winner_id != None:
				tournament.id_winner = match.winner_id
				match.winner_id.puntos += tournament.price_1
				match.winner_id.save()
			if match.looser_id != None:
				tournament.id_second = match.looser_id
				match.looser_id.puntos += tournament.price_2
				match.looser_id.save()
		elif match.round == Rounds.THIRD_PLACE_ROUND.value:
			if match.winner_id != None:
				tournament.id_third = match.winner_id
				match.winner_id.puntos += tournament.price_3
				match.winner_id.save()
	tournament.status = StatusTournaments.FINISHED_TOURNAMENT.value
	tournament.save()
