from __future__ import absolute_import
from datetime import timedelta
from tournamentsapp.models import Tournaments, Matches
from tournamentsapp.status_options import StatusMatches, Rounds, StatusTournaments
from tournamentsapp.tasks.create_matches import CreateMatches
from .finish_tournament import finish_tournament
from celery import shared_task
from tournaments.settings import TIME_DELTA
import uuid
import logging

logger = logging.getLogger('django')
@shared_task
def actualise_tournament(tournament_id):
	tournament = Tournaments.objects.get(id=mymatch.tournament_id)
	if tournament.status != StatusTournaments.CREATE_NEXT_ROUND.value:
		return
	match tournament.current_round:
		case 1:
			mymatch = Matches.objects.get(tournament_id=tournament_id, number_round=1, round=Rounds.FINAL_ROUND.value)
			logger.debug("Is Final round")
			tournament.id_winner = mymatch.winner_id
			tournament.id_second = mymatch.looser_id
			if mymatch.status != StatusMatches.ABORTED.value:
				mymatch.status = StatusMatches.NEXT_ROUND_ASSIGNED.value	
			logger.debug("Is third place round")
			mymatch = Matches.objects.get(tournament_id=tournament_id, number_round=1, round=Rounds.THIRD_PLACE_ROUND.value)
			tournament.id_third = mymatch.winner_id
			if mymatch.status != StatusMatches.ABORTED.value:
				mymatch.status = StatusMatches.NEXT_ROUND_ASSIGNED.value
			finish_tournament(tournament.id)
		case 2:
			logger.debug("Is semifinal round")
			mymatches = Matches.objects.get(
				tournament_id=tournament_id, 
				number_round=2, 
				round=Rounds.SEMIFINAL_ROUND.value,
				status__in=[StatusMatches.PLAYED.value, StatusMatches.WALKOVER.value])
			if mymatches.count() == 2:
				match_third = Matches.objects.create(
					tournament_id=mymatch.tournament_id,
					player_id_1=mymatches[0].looser_id if mymatches[0].looser_id !=  None else next_match[1].winner_id,
					player_id_2=mymatches[1].looser_id if mymatches[0].looser_id !=  None else None,
					date_time=tournament.last_match_date + timedelta(minutes=TIME_DELTA), 
					round=Rounds.THIRD_PLACE_ROUND.value,
					number_round=1,
					points_winner=tournament.winning_points,
					match_UUID = uuid.uuid4(),
					tournament_UUID = tournament.UUID,
					status = StatusMatches.NOT_PLAYED.value if mymatches[1].looser_id != None else StatusMatches.NEXT_ROUND_ASSIGNED.value)
				if(match_third.player_id_2 == None):
					match_third.status = StatusMatches.NEXT_ROUND_ASSIGNED.value
					match_third.winner_id = match_third.player_id_1
					match_third.save()
				elif match_third.player_id_1 == None and match_third.player_id_2 == None:
					match_third.status = StatusMatches.ABORTED.value
			else:
				match_third = Matches.objects.create(
					tournament_id=mymatch.tournament_id,
					player_id_1=None, 
					winner_id=None,
					player_id_2=None,
					looser_id=None, 
					date_time=tournament.last_match_date + timedelta(minutes=TIME_DELTA * 2), 
					round=Rounds.THIRD_PLACE_ROUND.value, 
					number_round=1,
					points_winner=tournament.winning_points,
					match_UUID = uuid.uuid4(),
					tournament_UUID = tournament.UUID,
					status = StatusMatches.ABORTED.value)
			if mymatches.count() >= 1:
				match_final = Matches.objects.create(
					tournament_id=mymatch.tournament_id,
					player_id_1=next_match[0].winner_id,
					player_id_2=next_match[1].winner_id, 
					date_time=tournament.last_match_date + timedelta(minutes=TIME_DELTA * 2), 
					round=Rounds.FINAL_ROUND.value, 
					number_round=1,
					points_winner=tournament.winning_points,
					match_UUID = uuid.uuid4(),
					tournament_UUID = tournament.UUID,
					status = StatusMatches.NOT_PLAYED.value)
			if(match_third.player_id_2 == None):
					match_final.status = StatusMatches.NEXT_ROUND_ASSIGNED.value
					match_final.winner_id = match_third.player_id_1
					match_final.save()
			elif match_third.player_id_1 == None and match_third.player_id_2 == None:
					match_final.status = StatusMatches.ABORTED.value
			else:
				tournament.status = StatusTournaments.ABORTED.value
			if mymatches[0].status != StatusMatches.ABORTED.value:
				mymatches[0].status = StatusMatches.NEXT_ROUND_ASSIGNED.value
			if mymatches[1].status != StatusMatches.ABORTED.value:
				mymatches[1].status = StatusMatches.NEXT_ROUND_ASSIGNED.value
			tournament.last_match_date += timedelta(minutes=TIME_DELTA * 2)
			tournament.current_round = 1
			tournament.save()
		case _:
			logger.debug("Is qualified round")
			next_match = Matches.objects.filter(
				tournament_id=mymatch.tournament_id, number_round=tournament.current_round, status__in=[StatusMatches.PLAYED.value, StatusMatches.WALKOVER.value])
			logger.debug(f"next_matches: {next_match.count()}, current round: {tournament.current_round} ")
			if next_match.count() <= 3:
				tournament.status = StatusTournaments.ABORTED.value
				tournament.save()
				for mymatch in next_match:
					mymatch.status = StatusMatches.ABORTED.value
					mymatch.save()			
				return
			tournament_players = []
			for mymatch in next_match:
				tournament_players.append(mymatch.winner_id)
			CreateMatches(tournament_id, tournament_players, extra_round = 0, current_round = tournament.current_round)


			"""
			get_out = 0
			while next_match.count() >= 2 and get_out<10:
				get_out += 1     
				for mymatch in next_match:
					logger.info(f"nextmatches:{mymatch.id} -- {mymatch.status} -- {mymatch.number_round}")
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
				if matches_not_played.count() == 0:
					tournament.current_round -= 1
				tournament.save()
				next_match = Matches.objects.filter(tournament_id=mymatch.tournament_id, round=Rounds.QUALIFIED_ROUND.value, status__in=[
                                    StatusMatches.PLAYED.value, StatusMatches.WALKOVER.value])
	return
"""