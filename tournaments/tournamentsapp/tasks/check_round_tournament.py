from tournamentsapp.models import Matches, Tournaments
from tournamentsapp.status_options import StatusMatches, StatusTournaments
import logging
logger = logging.getLogger('django')

def check_round_tournament(tournament_id):
	mymatches = Matches.objects.filter(
		tournament_id=tournament_id, 
		status__in=[StatusMatches.NOT_PLAYED.value, 
			  StatusMatches.WAITING_PLAYER1.value, 
			  StatusMatches.WAITING_PLAYER2.value, 
			  StatusMatches.STARTED.value])
	logger.debug(f'number of matches pending: {mymatches.count()}')
	if mymatches.count() == 0:
		tournament = Tournaments.objects.get(id=tournament_id)
		logger.debug(f'tournament {tournament.id} round number {tournament.round} passed to create next round')
		tournament.status = StatusTournaments.CREATE_NEXT_ROUND.value
		tournament.save()
		return True
	return False