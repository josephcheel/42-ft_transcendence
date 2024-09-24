from __future__ import absolute_import
from datetime import timedelta
from tournamentsapp.models import Tournaments, Matches
from tournamentsapp.status_options import StatusMatches, Rounds
from .finish_tournament import finish_tournament
from celery import shared_task
from tournaments.settings import TIME_DELTA

@shared_task
def actualise_tournament(match):
	tournament = Tournaments.objects.get(id=match.tournament_id)
	match (match.round):
		case Rounds.FINAL_ROUND.value:
			tournament.id_winner = match.winner_id
			tournament.id_second = match.looser_id
			match.status = StatusMatches.NEXT_ROUND_ASSIGNED.value
			finish_tournament.delay(tournament.id)
		case Rounds.THIRD_PLACE_ROUND.value:
			tournament.id_third = match.winner_id
			match.status = StatusMatches.NEXT_ROUND_ASSIGNED.value
		case Rounds.SEMIFINAL_ROUND.value:
			next_match = Matches.objects.filter(
				tournament_id=match.tournament_id, round=Rounds.SEMIFINAL_ROUND.value, status__in=[StatusMatches.PLAYED.value, StatusMatches.WALKOVER.value])
			if len(next_match) == 2:
				Matches.objects.create(
					tournament_id=match.tournament_id,player_id_1=next_match[0].looser_id,player_id_2=next_match[1].looser_id,date_time=tournament.last_match_date + timedelta(minutes=TIME_DELTA), round=Rounds.THIRD_PLACE_ROUND.value,
					number_round=1)
				Matches.objects.create(tournament_id=match.tournament_id, player_id_1=next_match[0].winner_id, player_id_2=next_match[
				                       1].winner_id, date_time=tournament.last_match_date + timedelta(minutes=TIME_DELTA * 2), round=Rounds.FINAL_ROUND.value, number_round=1)
				next_match[0].status = StatusMatches.NEXT_ROUND_ASSIGNED.value
				next_match[1].status = StatusMatches.NEXT_ROUND_ASSIGNED.value
				tournament.last_match_date += timedelta(minutes=TIME_DELTA * 2)
				tournament.current_round = 1
				tournament.save()
		case _:
			next_match = Matches.objects.filter(
				tournament_id=match.tournament_id, number_round=tournament.current_round, status__in=[StatusMatches.PLAYED.value, StatusMatches.WALKOVER.value])
			while len(next_match) >= 2:
				if tournament.current_round == 3:
					ronda_siguiente = Rounds.SEMIFINAL_ROUND.value
				else:
					ronda_siguiente = Rounds.QUALIFIED_ROUND.value
				Matches.objects.create(tournament_id=match.tournament_id, player_id_1=next_match[0].winner_id, player_id_2=next_match[1].winner_id,
				                       date_time=tournament.last_match_date + timedelta(minutes=TIME_DELTA), round=ronda_siguiente, number_round=tournament.current_round - 1)
				next_match[0].status = StatusMatches.NEXT_ROUND_ASSIGNED.value
				next_match[0].save()
				next_match[1].status = StatusMatches.NEXT_ROUND_ASSIGNED.value
				next_match[1].save()
				tournament.last_match_date += timedelta(minutes=TIME_DELTA)
				matches_not_played = Matches.objects.filter(
						tournament_id=match.tournament_id, number_round=tournament.current_round, status__in=[StatusMatches.NOT_PLAYED.value, StatusMatches.WALKOVER.value])
				if len(matches_not_played) == 0:
					tournament.current_round -= 1
				tournament.save()
				next_match = Matches.objects.filter(tournament_id=match.tournament_id, round=Rounds.QUALIFIED_ROUND.value, status__in=[
                                    StatusMatches.PLAYED.value, StatusMatches.WALKOVER.value])
	return
