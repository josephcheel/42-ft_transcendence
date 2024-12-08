from __future__ import absolute_import
from datetime import timedelta
from tournamentsapp.models import Tournaments, Matches
from tournamentsapp.status_options import StatusMatches, Rounds
from .finish_tournament import finish_tournament
from celery import shared_task
from tournaments.settings import TIME_DELTA
import uuid
import logging

logger = logging.getLogger('django')
@shared_task
def actualise_tournament(match_id):
	mymatch = Matches.objects.get(id=match_id)
	tournament = Tournaments.objects.get(id=mymatch.tournament_id)
	match (mymatch.round):
		case Rounds.FINAL_ROUND.value:
			logger.info("Is Final round")
			tournament.id_winner = mymatch.winner_id
			tournament.id_second = mymatch.looser_id
			if mymatch.status != StatusMatches.ABORTED.value:
				mymatch.status = StatusMatches.NEXT_ROUND_ASSIGNED.value
			finish_tournament(tournament.id)
		case Rounds.THIRD_PLACE_ROUND.value:
			logger.info("Is third place round")
			tournament.id_third = mymatch.winner_id
			if mymatch.status != StatusMatches.ABORTED.value:
				mymatch.status = StatusMatches.NEXT_ROUND_ASSIGNED.value
			finalmatch = Matches.objects.filter(
				tournament_id=mymatch.tournament_id, 
				round=Rounds.FINAL_ROUND.value, 
				status__in=[StatusMatches.PLAYED.value, StatusMatches.WALKOVER.value,StatusMatches.ABORTED.value])
			if len(finalmatch) == 1:
				finish_tournament(tournament.id)
		case Rounds.SEMIFINAL_ROUND.value:
			logger.info("Is semifinal round")
			next_match = Matches.objects.filter(
				tournament_id=mymatch.tournament_id, round=Rounds.SEMIFINAL_ROUND.value, status__in=[StatusMatches.PLAYED.value, StatusMatches.WALKOVER.value, StatusMatches.ABORTED.value])
			if len(next_match) == 2:
				match_third = Matches.objects.create(
					tournament_id=mymatch.tournament_id,
					player_id_1=next_match[0].looser_id,
					player_id_2=next_match[1].looser_id,
					date_time=tournament.last_match_date + timedelta(minutes=TIME_DELTA), 
					round=Rounds.THIRD_PLACE_ROUND.value,
					number_round=1,
					points_winner=tournament.winning_points,
					match_UUID = uuid.uuid4(),
					tournament_UUID = tournament.UUID)
				match_final = Matches.objects.create(
					tournament_id=mymatch.tournament_id,
					player_id_1=next_match[0].winner_id, 
					player_id_2=next_match[1].winner_id, 
					date_time=tournament.last_match_date + timedelta(minutes=TIME_DELTA * 2), 
					round=Rounds.FINAL_ROUND.value, 
					number_round=1,
					points_winner=tournament.winning_points,
					match_UUID = uuid.uuid4(),
					tournament_UUID = tournament.UUID)
				next_match[0].status = StatusMatches.NEXT_ROUND_ASSIGNED.value
				next_match[1].status = StatusMatches.NEXT_ROUND_ASSIGNED.value
				tournament.last_match_date += timedelta(minutes=TIME_DELTA * 2)
				tournament.current_round = 1
				tournament.save()
				if match_third.player_id_1 == None and match_third.player_id_2 == None:
					match_third.status = StatusMatches.ABORTED.value
					match_third.save()
				elif match_final.player_id_1 is not None and match_final.player_id_2 == None:
					match_final.status = StatusMatches.PLAYED.value
					match_final.save()
				else:
					match_third.status = StatusMatches.NOT_PLAYED.value
					match_final.save()
				if match_final.player_id_1 == None and match_final.player_id_2 == None:
					match_final.status = StatusMatches.ABORTED.value
					match_final.save()
				elif match_final.player_id_1 is not None and match_final.player_id_2 == None:
					match_final.status = StatusMatches.PLAYED.value
					match_final.save()
				else:
					match_final.status = StatusMatches.NOT_PLAYED.value
					match_final.save()
		case _:
			logger.info("Is qualified round")
			next_match = Matches.objects.filter(
				tournament_id=mymatch.tournament_id, number_round=tournament.current_round, status__in=[StatusMatches.PLAYED.value, StatusMatches.WALKOVER.value])
			logger.info(next_match)
			while len(next_match) >= 2:
				logger.info(next_match)
				if tournament.current_round == 3:
					ronda_siguiente = Rounds.SEMIFINAL_ROUND.value
				else:
					ronda_siguiente = Rounds.QUALIFIED_ROUND.value
				Matches.objects.create(
					tournament_id=mymatch.tournament_id, 
					player_id_1=next_match[0].winner_id, 
					player_id_2=next_match[1].winner_id,
				    date_time=tournament.last_match_date + timedelta(minutes=TIME_DELTA), 
					round=ronda_siguiente, 
					number_round=tournament.current_round - 1,
					points_winner=tournament.winning_points,
					match_UUID = uuid.uuid4(),
					tournament_UUID = tournament.UUID)
				next_match[0].status = StatusMatches.NEXT_ROUND_ASSIGNED.value
				next_match[0].save()
				next_match[1].status = StatusMatches.NEXT_ROUND_ASSIGNED.value
				next_match[1].save()
				tournament.last_match_date += timedelta(minutes=TIME_DELTA)
				matches_not_played = Matches.objects.filter(
						tournament_id=mymatch.tournament_id, number_round=tournament.current_round, status__in=[StatusMatches.NOT_PLAYED.value, StatusMatches.WALKOVER.value])
				if len(matches_not_played) == 0:
					tournament.current_round -= 1
				tournament.save()
				next_match = Matches.objects.filter(tournament_id=mymatch.tournament_id, round=Rounds.QUALIFIED_ROUND.value, status__in=[
                                    StatusMatches.PLAYED.value, StatusMatches.WALKOVER.value])
	return
