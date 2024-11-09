import requests
from datetime import datetime, timedelta
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



def get_csrf_token(session, url):
    # Step 1: Make a GET request to obtain CSRF cookie
    response = session.get(url)
    # The CSRF token is usually stored in the cookies
    csrf_token = response.cookies.get('csrftoken')
    return csrf_token

csrf_url = 'https://localhost:8000/api/get_cookie/'
login_url = 'https://localhost:8000/api/user/login_user/'
get_profile_url = 'https://localhost:8000/api/user/get_profile/1'
create_tournament_url = 'https://localhost:8000/api/tournaments/open_tournament/'
accept_invitation = 'https://localhost:8000/api/tournaments/accept_invitation/'
close_tournament = 'https://localhost:8000/api/tournaments/close/'
finish_match = 'https://localhost:8000/api/tournaments/finish_match/'
list_matches = 'https://localhost:8000/api/tournaments/list_matches/'
list_matches_username = 'https://localhost:8000/api/tournaments/list_matches/1'
create_user_url = 'https://localhost:8000/api/user/create_user/'
check_user_url = 'https://localhost:8000/api/user/check_user/'



session = requests.Session()
session.verify = False
csrf1 = get_csrf_token(session, csrf_url)
session2 = requests.Session()
session2.verify = False
csrf2 = get_csrf_token(session2, csrf_url)



def get_request(session, url, csrf_token, data=None):
    # Add CSRF token to the headers
    headers = {
        'Referer': 'https://localhost:8000',
        'X-CSRFToken': csrf_token,
        'Content-Type': 'application/json'
    }

    # Make the POST request to log in
    response = session.get(url, headers=headers)
    return response


def send_request(session, url, csrf_token, data=None):
    # Add CSRF token to the headers
    headers = {
        'Referer': 'https://localhost:8000',
        'X-CSRFToken': csrf_token,
        'Content-Type': 'application/json'
    }

    # Make the POST request to log in
    response = session.post(url, json=data, headers=headers)
    return response

# Main execution
if __name__ == "__main__":
    send_request(session, create_user_url, csrf1, {
        'username': 'test',
        'password': 'test',
        'first_name': 'test',
        'last_name': 'test',
        'email': 'test1@gmail.com'
    })

    send_request(session, create_user_url, csrf1, {
        'username': 'test1',
        'password': 'test',
        'first_name': 'test',
        'last_name': 'test',
        'email': 'test@gmail.com'
    })

    response1 = send_request(session, login_url, csrf1, {
        'username': "test",
        'password': "test"
    })

    response2 = send_request(session2, login_url, csrf2,{
        'username': "test1",
        'password': "test"
    })
    current_datetime = datetime.now()

    date_start = current_datetime + timedelta(days=1)

    date_start_iso = date_start.isoformat()

    response1 = send_request(session, create_tournament_url, csrf1,     {
		'date_start': date_start_iso,
        'max_players': 16,
        'cost': 10,
        'price_1': 100,
        'price_2': 50,
        'price_3': 25,
        'players': ['test','test1']
    })
    response1 = send_request(session, accept_invitation, csrf1, {
        'tournament_id': 1
    })
    response1 = send_request(session2, accept_invitation, csrf2, {
        'tournament_id': 1
    })
    response1 = send_request(session, close_tournament, csrf1, {
        'tournament_id': 1
    })

    response1 = send_request(session, finish_match, csrf1, {
        'match_id': '1',
        'winner': 'test1',
        'looser': 'test'
    })
    
    response1 = get_request(session, list_matches_username, csrf1)
    
    
    print(response1.json())
    session2.close()
    session.close()
