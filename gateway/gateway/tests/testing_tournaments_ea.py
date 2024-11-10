import requests
from datetime import datetime, timedelta
import urllib3
import json
import random
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#DOMAIN = '10.11.250.2'
DOMAIN = '192.168.40.44'


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
get_profile_url = f'https://{DOMAIN}:8000/api/user/get_profile'
create_tournament_url = f'https://{DOMAIN}:8000/api/tournaments/open_tournament/'
accept_invitation = f'https://{DOMAIN}:8000/api/tournaments/accept_invitation/'
close_tournament = f'https://{DOMAIN}:8000/api/tournaments/close/'
finish_match = f'https://{DOMAIN}:8000/api/tournaments/finish_match/'
list_matches = f'https://{DOMAIN}:8000/api/tournaments/list_matches/'
list_matches_username = f'https://{DOMAIN}:8000/api/tournaments/list_matches/1'
total_players = 8




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
		print(response.status_code, response.json())
		if response.status_code == 201:
			assert response.json()['status'] == 'success'
			assert response.json()['message'] == 'User created successfully'
		else:
			assert response.status_code == 409
			assert response.json()['status'] == 'error'
			assert response.json()['message'] == 'User already Exists'
		my_data = {'username': f"test{i}", 'password': "test"}
		response = send_request(mysessions[i], login_url, csrf[i], my_data)
		print(response.status_code, response.json())
		assert response.status_code == 200
		assert response.json()['status'] == 'success'
		assert response.json()['message'] == 'user is logged in'
		response = send_request(
			mysessions[i], get_profile_url + '/' + f"test{i}", csrf[i])
		print(response.status_code, response.json())
		assert response.status_code == 200
		assert response.json()['status'] == 'success'
		assert response.json()['message'] == 'Got user profile'
		assert response.json()['data']['username'] == f'test{i}'

def play_match():
	print("log in all players")
	for i in range(1, total_players + 1):
		my_data = {'username': f"test{i}", 'password': "test"}
		response = send_request(mysessions[i], login_url, csrf[i], my_data)
	for i in range(1, 100):
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
		response = send_request(mysessions[user_nr1], finish_match, csrf[user_nr1], data = my_data)
		print(response.status_code, response.json())
		assert response.status_code == 200
		assert response.json()['status'] == 'success'
		assert response.json()['message'] == 'Match finished successfully'

def close_sessions():
	for i in range(1, total_players + 1):
		mysessions[i].close()
# Main execution
if __name__ == "__main__":
	test_register_user()
	play_match()
	close_sessions()

