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
	tournament = Tournaments.objects.get(id=tournament_id)
	if tournament.status != StatusTournaments.CREATE_NEXT_ROUND.value:
		return
	match tournament.current_round:
		# We are in the final round
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
			logger.debug("Is final round i finish the turnament")
			finish_tournament(tournament.id)
		# We are at the semifinal round
		case 2:
			logger.debug("Is semifinal round")
			mymatches = Matches.objects.filter(
				status__in=[StatusMatches.NOT_PLAYED.value, 
							StatusMatches.WAITING_PLAYER1.value, 
							StatusMatches.WAITING_PLAYER2.value])
			if mymatches.count() > 0:
				return
			mymatches = Matches.objects.filter(
				tournament_id=tournament_id, 
				number_round=2, 
				round=Rounds.SEMIFINAL_ROUND.value,
				status__in=[StatusMatches.PLAYED.value, StatusMatches.WALKOVER.value])
			# If I have 2 matches then I can just create the third match with the players
			# If I dont have exactly 2 matches then I need to create the third (final) match in a
			# aborted state
			if mymatches.count() == 2:
				match_third = Matches.objects.create(
					tournament_id=mymatches[0].tournament_id,
					player_id_1=mymatches[0].looser_id if mymatches[0].looser_id !=  None else mymatches[1].winner_id,
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
				elif match_third.player_id_1 == None and match_third.player_id_2 == None:
					match_third.status = StatusMatches.ABORTED.value
				match_third.save()
			else:
				match_third = Matches.objects.create(
					tournament_id=tournament_id,
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
			
			# There can 0, 1 or 2 matches. 0 if both are aborted 1 or 2 if they are OKAY
			# We need to create the final round if it's not equal to 0
			if mymatches.count() != 0:
				match_final = Matches.objects.create(
					tournament_id=mymatches[0].tournament_id,
					player_id_1=mymatches[0].winner_id,
					player_id_2= mymatches[0].looser_id if mymatches.count() == 1 else  mymatches[1].looser_id, 
					winner_id=mymatches[0].winner_id,
					looser_id=mymatches[0].looser_id,
					date_time=tournament.last_match_date + timedelta(minutes=TIME_DELTA * 2), 
					round=Rounds.FINAL_ROUND.value, 
					number_round=1,
					points_winner=tournament.winning_points,
					match_UUID = uuid.uuid4(),
					tournament_UUID = tournament.UUID,
					status = StatusMatches.NOT_PLAYED.value)
				
				# We check final match. If there is no player id 2 then there is only one player,
				# so the player we do have wins
				if match_final.player_id_2 == None:
						match_final.status = StatusMatches.NEXT_ROUND_ASSIGNED.value
						match_final.winner_id = match_final.player_id_1
						match_final.save()
			# if mymatches == 0 then there are no valid matches before this, so the whole tournament goes to aborted
			else:
				match_final = Matches.objects.create(
					tournament_id=tournament_id,
					player_id_1=None,
					player_id_2= None, 
					date_time=tournament.last_match_date + timedelta(minutes=TIME_DELTA * 2), 
					round=Rounds.FINAL_ROUND.value, 
					number_round=1,
					points_winner=tournament.winning_points,
					match_UUID = uuid.uuid4(),
					tournament_UUID = tournament.UUID,
					status = StatusMatches.ABORTED.value)
				logger.debug("Is aborted line 93")
				tournament.status = StatusTournaments.ABORTED.value
				tournament.save()
			
			# We close the semi final round with NEXT ROUND 
			if mymatches.count() >= 1:
				mymatches[0].status = StatusMatches.NEXT_ROUND_ASSIGNED.value
				mymatches[0].save()
			if mymatches.count() == 2:
				mymatches[1].status = StatusMatches.NEXT_ROUND_ASSIGNED.value
				mymatches[1].save()
			tournament.last_match_date += timedelta(minutes=TIME_DELTA * 2)
			tournament.current_round = 1
			tournament.save()
			if mymatches.count() <= 0:
				finish_tournament(tournament.id)
				
		# This is everythin that's not final or semifinal
		case _:
			logger.debug("Is qualified round")
			mymatches = Matches.objects.filter(
				tournament_id=tournament_id, number_round=tournament.current_round, status__in=[StatusMatches.PLAYED.value, StatusMatches.WALKOVER.value])
			logger.debug(f"mymatcheses: {mymatches.count()}, current round: {tournament.current_round} ")
			# We don't have enough matches to finish this tournament, we abort everything
			if mymatches.count() <= 3:
				logger.debug("Is aborted line 108")
				tournament.status = StatusTournaments.ABORTED.value
				tournament.save()
				for mymatch in mymatches:
					logger.debug("Is aborted line 112")
					mymatch.status = StatusMatches.ABORTED.value
					mymatch.save()			
				return
			tournament_players = []
			for mymatch in mymatches:
				tournament_players.append(mymatch.winner_id)
			CreateMatches(tournament_id, tournament_players, extra_round = 0, current_round = tournament.current_round)


			"""
			get_out = 0
			while mymatches.count() >= 2 and get_out<10:
				get_out += 1     
				for mymatch in mymatches:
					logger.info(f"nextmatches:{mymatch.id} -- {mymatch.status} -- {mymatch.number_round}")
				if tournament.current_round == 3:
					ronda_siguiente = Rounds.SEMIFINAL_ROUND.value
				else:
					ronda_siguiente = Rounds.QUALIFIED_ROUND.value
				Matches.objects.create(
					tournament_id=mymatch.tournament_id, 
					player_id_1=mymatches[0].winner_id, 
					player_id_2=mymatches[1].winner_id,
				    date_time=tournament.last_match_date + timedelta(minutes=TIME_DELTA), 
					round=ronda_siguiente, 
					number_round=tournament.current_round - 1,
					points_winner=tournament.winning_points,
					match_UUID = uuid.uuid4(),
					tournament_UUID = tournament.UUID)
				mymatches[0].status = StatusMatches.NEXT_ROUND_ASSIGNED.value
				mymatches[0].save()
				mymatches[1].status = StatusMatches.NEXT_ROUND_ASSIGNED.value
				mymatches[1].save()
				tournament.last_match_date += timedelta(minutes=TIME_DELTA)
				matches_not_played = Matches.objects.filter(
						tournament_id=mymatch.tournament_id, number_round=tournament.current_round, status__in=[StatusMatches.NOT_PLAYED.value, StatusMatches.WALKOVER.value])
				if matches_not_played.count() == 0:
					tournament.current_round -= 1
				tournament.save()
				mymatches = Matches.objects.filter(tournament_id=mymatch.tournament_id, round=Rounds.QUALIFIED_ROUND.value, status__in=[
                                    StatusMatches.PLAYED.value, StatusMatches.WALKOVER.value])
	return
"""