# Table of contents
| Section | Links |
|---------|-------|
| [User](#user) | [create_user](#create_user) <br> [login_user](#login_user) <br> [logout_user](#logout_user) <br> [is_logged_in](#is_logged_in) <br> [list_users](#list_users) <br> [user_status](#user_status) <br> [send_friend_request](#send_friend_request)<br> [change_friendship_status](#change_friendship_status)<br> [get_friends](#get_friends)<br> [update_user](#update_user) | [Match](#match) | [propose_match](#propose_match) <br> [get_pending_matches](#get_pending_matches) | [open_tournament] (#open_tournament) | [accept_invitation] (#accept_invitation) | [close_tournament](#close_tournament) | [start_match](#start_match) | [finish_match](#finish_match)



All API calls will return a json response and the corresponding code

json response format:

{
    'status' : 'error' / 'success',
    'message' : A short message,
    'data' : None / 'Data'

}
## User

user/[subpath]

### create_user

| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
| Creates User if not in the database. | POST | {username, password, tournament_name} | None |  201, 409 (already exists), 400, 405, 500 |

[Back to Top](#table-of-contents)



### login_user

| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
| Logs in User| POST | None (cookies handles it) | None |200, 400, 401 (invalid credentials), 405, 500|

[Back to Top](#table-of-contents)


### logout_user

| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
| Logs out User| POST | None (cookies handles it) | None |200, 403 ( Forbidden), 405, 500|

[Back to Top](#table-of-contents)


### is_logged_in


| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
| Checks if YOUR user is logged in | GET | None | None |  200 (user logged in), 401 (Unauthorized), 405, 500|

[Back to Top](#table-of-contents)


### list_users

| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
| Returns a list of all users registered | GET | None | List of users. Each element inside the list is a dictionaty with id and username keys |  200 (user logged in), 405, 500|

[Back to Top](#table-of-contents)


### user_status

| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
| Returns current online status of user | GET | username | is_online: True/False |  200 , 404 (user not found), 405, 500|
| Changes current user status | POST | status: online/offline | None |  200, 400(invalid json or user not auth), 404 (user not found), 405, 500|

[Back to Top](#table-of-contents)


### send_friend_request

| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
| Sends friend request | POST | username to send request  | None |  201 ,400, 401,404 (user not found), 405, 500|

[Back to Top](#table-of-contents)

### change_friendship_status

| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
| Updates friendship | POST | username: friend, status: [accepted / declined]  | None |  200 ,400, 401,404 (user not found or no friendship), 405, 500|


[Back to Top](#table-of-contents)

### get_friends

| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
| gets friends list | GET | None | lista de diccionarios (puede estar vacia): <br> {username, <br>friendship (accepted/pending/declined),<br> is_online(True,False)}  |  200,401,405,500|


[Back to Top](#table-of-contents)


### update_user

| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
| Updates user fields: first_name, last_name, tournament_name | POST | first_name, last_name, tournament_name | None |  200,400,401,405, 500|


[Back to Top](#table-of-contents)

## Tournaments

tournaments/[subpath]

### open_tournament

| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
| Creates a tournament and sends invitation to all players  | POST | 'username', <BR>'password'
			'date_start', <BR> 'max_players', <BR> 'cost', <BR> 'price_1', <BR> 'price_2', <BR> 'price_3', <BR> 'players':[username1, username2, ...]	 | None |  200 (tournament created), 400 (incorrect data), 404 (user not in database), 500|

### accept_invitation
| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
|Payer accepts the invitation to a turnaament| POST | 'username' 'password' 'tournament_id' | None |  200 (invitation accepted), 400 (incorrect data), 404 (user not in database), 500|

### close tournament (to start tournament)
| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
|Payer accepts the invitation to a turnaament| POST | 'username' 'password' 'tournament_id' | None |  200 (invitation accepted), 400 (incorrect data), 404 (user not in database), 500|

### start match
| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
|When the first player access to the match| POST | 'username' 'password' 'tournament_id' | None |  200 (invitation accepted), 400 (incorrect data), 404 (user not in database), 500|

### finish match
| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
|When the match finishes, informs who is the winner| POST | 'match_id' 'winner' 'looser' | None |  200 (Match finished successfully), 400 (he match has already been played), 404 (user not in database), 500|

## Match

match/[subpath]

### propose_match

| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
| Sends invitation to all players | POST | start_time, players[first player is the owner/creator] | None |  200 (user logged in), 400, 404 (user not in database), 500|

[Back to Top](#table-of-contents)


### get_pending_matches

| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
| Checks if user has pending matches to accept | GET | player (in query) | List of pending invitations or empty list |  200 , 400, 404 (user not in database), 500|

[Back to Top](#table-of-contents)
