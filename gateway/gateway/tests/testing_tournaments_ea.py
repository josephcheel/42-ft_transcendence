import requests
from datetime import datetime, timedelta
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
DOMAIN = '10.11.250.2'
#DOMAIN = 'localhost'


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
get_profile_url = f'https://{DOMAIN}:8000/api/user/get_profile/1'
create_tournament_url = f'https://{DOMAIN}:8000/api/tournaments/open_tournament/'
accept_invitation = f'https://{DOMAIN}:8000/api/tournaments/accept_invitation/'
close_tournament = f'https://{DOMAIN}:8000/api/tournaments/close/'
finish_match = f'https://{DOMAIN}:8000/api/tournaments/finish_match/'
list_matches = f'https://{DOMAIN}:8000/api/tournaments/list_matches/'
list_matches_username = f'https://{DOMAIN}:8000/api/tournaments/list_matches/1'





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

#Test and create 21 users
def test_register_user():
    for i in range(1, 22):
        mysessions[i] = requests.Session()
        mysessions[i].verify = False
        csrf[i] = get_csrf_token(mysessions[i], csrf_url)
        my_data = json.dumps({'username': f"test{i}", 'password': "test", 'first_name': f"test{i}",  'last_name': f"Apellido{i}"})
        response = send_request(mysessions[i], register_url, csrf[i], my_data)
        print(response.json())
        print(csrf[i])
        assert response.status_code == 201
        assert response.json()['status'] == 'success'
        assert response.json()['message'] == 'User created successfully'
        my_data = json.dumps({'username': f"test{i}", 'password': "test"})
        response = send_request(mysessions[i], login_url, csrf[i], my_data)
        assert response.status_code == 200
        assert response.json()['status'] == 'success'
        assert response.json()['message'] == 'User logged in successfully'
        response = send_request(mysessions[i], get_profile_url, csrf[i])
        assert response.status_code == 200
        assert response.json()['status'] == 'success'
        assert response.json()['message'] == 'User profile retrieved successfully'
        assert response.json()['data']['username'] == f'test{i}'

def close_sessions():
    for i in range(1, 22):
        mysessions[i].close()
# Main execution
if __name__ == "__main__":
    test_register_user()
    close_sessions()
    """response1 = send_request(session, login_url, csrf1, {
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
        'tournament_id': 2
    })
    response1 = send_request(session2, accept_invitation, csrf2, {
        'tournament_id': 2
    })
    response1 = send_request(session, close_tournament, csrf1, {
        'tournament_id': 2
    })

    response1 = send_request(session, finish_match, csrf1, {
        'match_id': '2',
        'winner': 'test1',
        'looser': 'test'
    }) 

    response1 = get_request(session, list_matches_username, csrf1)
    
    
    print(response1.json())
    session2.close()
    session.close()
"""
