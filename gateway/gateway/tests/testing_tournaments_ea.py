import requests
from datetime import datetime, timedelta
from django.utils import timezone
import urllib3
import json
import random
import pytz

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#DOMAIN = '10.11.250.2'
DOMAIN = '192.168.40.44'
EuropeZone = pytz.timezone('Europe/Madrid')

def get_csrf_token(session, url):
	# Step 1: Make a GET request to obtain CSRF cookie
	response = session.get(url)
	# The CSRF token is usually stored in the cookies
	csrf_token = response.cookies.get('csrftoken')
	return csrf_token

content_json_type = 'application/json'
referer = f'https://{DOMAIN}:8000'
csrf_url = f'https://{DOMAIN}:8000/api/get_cookie/'
register_url = f'https://{DOMAIN}:8000/api/user/create_user/'
login_url = f'https://{DOMAIN}:8000/api/user/login_user/'
logout_url = f'https://{DOMAIN}:8000/api/user/logout_user/'
get_profile_url = f'https://{DOMAIN}:8000/api/user/get_profile'
create_tournament_url = f'https://{DOMAIN}:8000/api/tournaments/open_tournament/'
accept_invitation = f'https://{DOMAIN}:8000/api/tournaments/accept_invitation/'
close_tournament = f'https://{DOMAIN}:8000/api/tournaments/close/'
finish_match_url = f'https://{DOMAIN}:8000/api/tournaments/finish_match/'
list_matches_url = f'https://{DOMAIN}:8000/api/tournaments/list_matches/'
list_matches_by_tournament_id_url = f'https://{DOMAIN}:8000/api/tournaments/list_matches_by_tournament_id/'
list_invitations = f'https://{DOMAIN}:8000/api/tournaments/list_invitations/'
list_tournaments_url = f'https://{DOMAIN}:8000/api/tournaments/list_tournaments/'
start_match_url = f'https://{DOMAIN}:8000/api/tournaments/start_match/'
total_players = 22
total_matches = 100
total_tournaments = 5

def get_request(session, url, csrf_token, data=None):
	# Add CSRF token to the headers
	headers = {
		'Referer': referer,
		'X-CSRFToken': csrf_token,
		'Content-Type': content_json_type
	}

	# Make the POST request to log in
	response = session.get(url, headers=headers)
	return response


def send_request(session, url, csrf_token, data=None):
	# Add CSRF token to the headers
	headers = {
		'Referer': referer,
		'X-CSRFToken': csrf_token,
		'Content-Type': content_json_type
	}

	# Make the POST request to log in
	response = session.post(url, json=data, headers=headers)
	return response


mysessions = {}
csrf = {}

#Test and create total_players users
def test_register_user():
	for i in range(1, total_players + 1):
		mysessions[i] = requests.Session()
		mysessions[i].verify = False
		csrf[i] = get_csrf_token(mysessions[i], csrf_url)
		my_data = {'username': f"test{i}", 'password': "test", 'first_name': f"test{i}",  'last_name': f"Apellido{i}"}
		response = send_request(mysessions[i], register_url, csrf[i], my_data)
		if response.status_code == 201:
			assert response.json()['status'] == 'success'
			assert response.json()['message'] == 'User created successfully'
		else:
			assert response.status_code == 409
			assert response.json()['status'] == 'error'
			assert response.json()['message'] == 'User already Exists'
		my_data = {'username': f"test{i}", 'password': "test"}
		response = send_request(mysessions[i], login_url, csrf[i], my_data)
		assert response.status_code == 200
		assert response.json()['status'] == 'success'
		assert response.json()['message'] == 'user is logged in'
		response = send_request(
			mysessions[i], get_profile_url + '/' + f"test{i}", csrf[i])
		print(f"User test{i} created and logged in with profile :{response.json()}")
		assert response.status_code == 200
		assert response.json()['status'] == 'success'
		assert response.json()['message'] == 'Got user profile'
		assert response.json()['data']['username'] == f'test{i}'

def play_match():
	print("log in all players")
	for i in range(1, total_players + 1):
		my_data = {'username': f"test{i}", 'password': "test"}
		response = send_request(mysessions[i], login_url, csrf[i], my_data)
	for i in range(1, total_matches + 1):
		user_nr1 = random.randint(1, total_players)
		player1 = f"test{user_nr1}"
		player2 = f"test{random.randint(1, total_players)}"
		while player1 == player2:
			player2 = f"test{random.randint(1, total_players)}"
		winning_points = 5
		looser_points = random.randint(0, winning_points-1)
		if random.choice([True, False]):
			my_data = {
				'match_id': -1,
				'player1': player1,
				'player2': player2,
				'winner': player1,
				'looser': player2,
				'points_winner': winning_points,
				'points_looser': looser_points,
			}
			text_to_print = f"Played match {i} between {player1} and {player2}, result:  {player1}:{winning_points} - {player2}:{looser_points}"
		else:
			my_data = {
				'match_id': -1,
				'player1': player1,
				'player2': player2,
				'winner': player2,
				'looser': player1,
				'points_winner': winning_points,
				'points_looser': looser_points,
			}
			#text_to_print = f"Played match {i} between {player1} and {player2}, result:  {player2}:{winning_points} - {player1}:{looser_points}"
		response = send_request(mysessions[user_nr1], finish_match_url, csrf[user_nr1], data = my_data)
		#print(text_to_print, "-------", response.json())
		assert response.status_code == 200
		assert response.json()['status'] == 'success'
		assert response.json()['message'] == 'Match finished successfully'
	for i in range(1, total_players + 1):
		response= get_request(mysessions[i], list_matches_url + f"test{i}", csrf[i])
		print(f"User test{i} list of matches: {response.json()}")

def test_create_tournament():
	for i in range(1, total_tournaments + 1):
		player_nr = random.randint(1, total_players)
		players = []
		for j in range(1, random.randint(5, total_players)):
			the_player = random.randint(1, total_players)
			while f'test{the_player}' in players:
				#print(f"{the_player} is in players: {players}")
				the_player = random.randint(1, total_players)
			players.append(f'test{the_player}')
			j += 1
		#print(f"players: {players}")
		my_data = {
			"name" : f'test_tournament_{j}',
            'username': f'test{player_nr}',
            'password': 'test',
            'date_start': (datetime.now(EuropeZone) + timedelta(minutes=1)).isoformat(),
            'max_players': total_players,
            'cost': 1,
            'price_1': 1000,
            'price_2': 500,
            'price_3': 250,
            'players': players, }
		response = send_request(mysessions[4], create_tournament_url, csrf[4], my_data)
		print(f"test _torunament_{j} created {response.json()}")
		assert response.status_code == 200
		assert response.json()['status'] == 'success'
		assert response.json()['message'] == 'Tournament created successfully'

def test_accept_invitation():
	for i in range (1, total_players + 1):
		user_data = {'username': f"test{i}", 'password': "test"}
		response = send_request(mysessions[i], login_url, csrf[i], user_data)
		assert response.status_code == 200
		response=get_request(mysessions[i], list_invitations + f"test{i}" , csrf[i])
		print(list_invitations + f"test{i}")
		print(f"User test{i} list of invitations: {response.json()}")
		invitation_list = json.loads(response.json()['data'])
		if invitation_list == []:
			print(f"User test{i} has no invitations")
		else:
			for invitation in invitation_list:
				print ("La invitacion es:  ", invitation)
				if random.uniform(0, 1) >0.3:
					if invitation['status'] == 'ignored':
						my_data = {
						'tournament_id': invitation['tournament_id_id']
						}
						response = send_request(mysessions[i], accept_invitation, csrf[i], my_data)
						print ("data_sent     " , my_data)
						print(f"User test{i} accepted 	invitation {response.json()}")
						assert response.status_code == 200
						assert response.json()['status'] == 'success'
						assert response.json()['message'] == 'Invitation accepted successfully'
		user_data = {'username': f"test{i}", 'password': "test"}
		response = send_request(mysessions[i], logout_url, csrf[i], user_data)

def test_close_tournament():
	for i in range(1, total_players + 1):
		my_data = {'username': f"test{i}", 'password': "test"}
		response = send_request(mysessions[i], login_url, csrf[i], my_data)
		assert response.status_code == 200
		response = get_request(mysessions[i], list_tournaments_url + f"test{i}", csrf[i])
		print(f"User test{i} list of tournaments: {response.json()}")
		list_tournaments = json.loads(response.json()['data'])
		if list_tournaments == []:
			print(f"User test{i} has no tournaments")
		else:
			for tournament in list_tournaments:
				if tournament['status'] == 'open' and random.uniform(0, 1) > 0.3:
					my_data = {
					"tournament_id": tournament['id']
					}
					response = send_request(mysessions[4], close_tournament, csrf[4], my_data)
					print(f"Tournament {i} closed {response.json()}")
					assert response.status_code == 200
					assert response.json()['status'] == 'success'
					assert response.json()['message'] == 'Tournament closed successfully'
	user_data = {'username': f"test{i}", 'password': "test"}
	response = send_request(mysessions[i], logout_url, csrf[i], user_data)

def test_finish_tournament():
	for i in range(1, total_players + 1):
		user_data = {'username': f"test{i}", 'password': "test"}
		response = send_request(mysessions[i], login_url, csrf[i], user_data)
		assert response.status_code == 200

	for i in range(1, total_players + 1):
		response = get_request(
			mysessions[i], list_tournaments_url + f"test{i}", csrf[i])
		list_tournaments = json.loads(response.json()['data'])
		if list_tournaments == []:
			print(f"User test{i} has no tournaments")
		else:
			print(f"User test{i} list of tournaments: {response.json()}")
			for tournament in list_tournaments:
				tournament_id = tournament['id']
				response = get_request(
					mysessions[i], list_matches_by_tournament_id_url + f"{tournament_id}", csrf[i])
				list_matches = json.loads(response.json()['data'])
				while list_matches != []:
					for match in list_matches:
						player1 = match['player_id_1']
						player2 = match['player_id_2']
						my_data = {'match_id': match['id']}
						if random.choice([True, False]):
							response = send_request(mysessions[int(player1)], start_match_url, csrf[int(player1)], my_data)
							assert response.status_code == 200
							assert response.json()['status'] == 'success'
							assert response.json()['message'] == 'Waiting for player 2 to start the match'
							response = send_request(
								mysessions[int(player2)], start_match_url, csrf[int(player2)], my_data)
							assert response.status_code == 200
							assert response.json()['status'] == 'success'
							assert response.json()['message'] == 'Match started successfully'
						else:
							response = send_request(
								mysessions[int(player2)], start_match_url, csrf[int(player2)], my_data)
							assert response.status_code == 200
							assert response.json()['status'] == 'success'
							assert response.json()[                                                          'message'] == 'Waiting for player 1 to start the match'
							response = send_request(
								mysessions[int(player1)], start_match_url, csrf[int(player1)], my_data)
							assert response.status_code == 200
							assert response.json()['status'] == 'success'
							assert response.json()['message'] == 'Match started successfully'

						print('match =', match['id'], ' started!!!! player1 =',
						      f'test{player1}', ' player2 =', f'test{player2}')
						if random.choice([True, False]):
							the_winner_id = f'test{player1}'
							the_looser_id = f'test{player2}'
						else:
							the_winner_id = f'test{player2}'
							the_looser_id = f'test{player1}'
						my_data = {
                            'match_id': -1,
                            'player1': f'test{player1}',
                            'player2': f'test{player2}',
                            'winner': the_winner_id,
                            'looser': the_winner_id,
                            'points_winner': int(tournament['winning_points']),
                            'points_looser': random.randint(0, int(tournament['winning_points'])-1)
                        	}
						response = send_request(
							mysessions[player1], finish_match_url, csrf[player1], data=my_data)
						assert response.status_code == 200
						assert response.json()['status'] == 'success'
						assert response.json()['message'] == 'Match finished successfully'

						print('match =', match.id, ' finished. Won!!!!',
							the_winner_id, ' lost ', the_looser_id)
						response = get_request(
                    mysessions[i], list_matches_by_tournament_id_url + f"{tournament_id}", csrf[i])
					list_matches = json.loads(response.json()['data'])

					

def close_sessions():
	for i in range(1, total_players + 1):
		mysessions[i].close()

# Main execution
if __name__ == "__main__":
	test_register_user()
	play_match()
	test_create_tournament()
	test_accept_invitation()
	test_close_tournament()
	test_finish_tournament()
	close_sessions()

