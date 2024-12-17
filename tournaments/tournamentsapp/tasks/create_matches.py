from datetime import datetime, timedelta
from tournamentsapp.models import Tournaments, Matches
from tournamentsapp.status_options import StatusMatches, Rounds
from tournaments.settings import TIME_DELTA
import math
import uuid
from user.models import User


def CreateMatches(tournament_id, tournament_players:User, extra_round, current_round):
	tournament = Tournaments.objects.get(id=tournament_id)
	next_match_date = tournament.last_match_date
	player_nr = tournament_players.count()
	match player_nr:
		case 2:
			Matches.objects.create(
				tournament_id = tournament_id, 
				number_round = 1, 
				date_time = next_match_date,
				player_id_1 = tournament_players[0].player_id,
				points_winner = tournament.winning_points,
				player_id_2 = tournament_players[1].player_id,
				round=Rounds.FINAL_ROUND.value,
				match_UUID = uuid.uuid4(),
				tournament_UUID = tournament.UUID)
			tournament_players[0].player_id.puntos_reservados -= tournament.cost
			tournament_players[0].player_id.save()
			tournament_players[1].player_id.puntos_reservados -= tournament.cost
			tournament_players[1].player_id.save()
			tournament.current_round = 1
		case 4:
			Matches.objects.create(
				tournament_id = tournament_id,
				number_round = 2,
				date_time = next_match_date,
				player_id_1 = tournament_players[0].player_id,
				player_id_2 = tournament_players[1].player_id,
				points_winner=tournament.winning_points,
				round=Rounds.SEMIFINAL_ROUND.value,
				match_UUID = uuid.uuid4(),
				tournament_UUID = tournament.UUID)
			tournament_players[0].player_id.puntos_reservados -= tournament.cost
			tournament_players[0].player_id.save()
			tournament_players[1].player_id.puntos_reservados -= tournament.cost
			tournament_players[1].player_id.save()
			next_match_date += timedelta(minutes=TIME_DELTA)
			Matches.objects.create(
				tournament_id=tournament_id,
				number_round=2,
				date_time=next_match_date,
				player_id_1=tournament_players[2].player_id,
				player_id_2=tournament_players[3].player_id,
				points_winner=tournament.winning_points,
				round=Rounds.SEMIFINAL_ROUND.value,
				match_UUID = uuid.uuid4(),
				tournament_UUID = tournament.UUID)
			tournament_players[2].player_id.puntos_reservados -= tournament.cost
			tournament_players[2].player_id.save()
			tournament_players[3].player_id.puntos_reservados -= tournament.cost
			tournament_players[3].player_id.save()
			tournament.current_round = 2
		case _:
			numero_partidos = int(math.pow(2, current_round + extra_round -1)) 
			for i in range (0, numero_partidos):
				tournament_players[i].player_id.puntos_reservados -= tournament.cost
				tournament_players[i].player_id.save()
				try:
					player_2 = tournament_players[i + numero_partidos].player_id
					player_2.puntos_reservados  -= tournament.cost
					player_2.save()
					status = StatusMatches.NOT_PLAYED.value
					player_winner = None
				except:
					player_2 = None
					player_winner = tournament_players[i].player_id
					status = StatusMatches.WALKOVER.value

				Matches.objects.create(
					tournament_id = tournament_id,
					date_time = next_match_date,
					player_id_1 = tournament_players[i].player_id,
					player_id_2 = player_2,
					winner_id = player_winner,
                    points_winner=tournament.winning_points,
					round=Rounds.QUALIFIED_ROUND.value,
					number_round = current_round + extra_round,
					status=status,
					match_UUID = uuid.uuid4(),
					tournament_UUID = tournament.UUID)
				next_match_date += timedelta(minutes=TIME_DELTA)
			tournament.current_round = current_round + extra_round
	return next_match_date