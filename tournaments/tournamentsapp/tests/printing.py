from tournamentsapp.models import Tournaments, Invitations, Matches, User
from user.models import User
from blockchainapp.views import get_balance_from_web3

def print_all_tournaments():
	print('Tournaments list')
	tournaments = Tournaments.objects.all()
	for tournament in tournaments:
		print('tournament_id: ', tournament.id, 'player_id: ', tournament.player_id, 'cost: ', tournament.cost, 'price_1: ', tournament.price_1, 'price_2: ', tournament.price_2, 'price_3: ', tournament.price_3, 'id_winner: ', tournament.id_winner, 'id_second: ', tournament.id_second, 'id_third: ', tournament.id_third, 'status: ', tournament.status, 'current_round: ', tournament.current_round)

def print_all_invitations():
	print('Invitations list')
	invitations = Invitations.objects.all()
	for invitation in invitations:
		print('invitation_id: ', invitation.id, 'tournament_id: ', invitation.tournament_id, 'player_id: ', invitation.player_id, 'status: ', invitation.status)

def print_all_matches():
	print('Matches list')
	matches = Matches.objects.all()
	for match in matches:
		print('match_id: ', match.id, 'tournament_id: ', match.tournament_id, 'player_id_1: ', match.player_id_1, 'player_id_2: ', match.player_id_2, 'winner_id: ', match.winner_id, 'loser_id: ', match.looser_id, 'round: ', match.round, 'status: ', match.status, 'nr_round: ', match.number_round)

def print_all_users():
	print('Users list')
	users = User.objects.all()
	for user in users:
		print('user_id: ', user.id, 'username: ', user.username, 'email: ', user.email, 'puntos: ', user.puntos, 'puntos_reservados: ', user.puntos_reservados
                    , 'wallet = ',  user.ethereum_address, 'wallet balance = ',  get_balance_from_web3(user.ethereum_address))
