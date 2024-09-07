# Table of contents
| Section | Links |
|---------|-------|
| [User](#user) | [create_user](#create_user) <br> [login_user](#login_user) <br> [logout_user](#logout_user) <br> [is_logged_in](#is_logged_in) |
| [Match](#match) | [propose_match](#propose_match) <br> [get_pending_matches](#get_pending_matches) | [open_tournement] (#open_tournement) | [accept_invitation] (#accept_invitation) | [close_tournement](#close_tournement) | [start_match](#start_match) | [finish_match](#finish_match)


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
| Creates User if not in the database. | POST | {username, password} | {user id, username (same as in request data)} |  201, 409 (already exists), 400, 405, 500 |

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
| Checks if YOUR user is logged in | GET | username | None |  200 (user logged in), 401 (Unauthorized), 405, 500|


[Back to Top](#table-of-contents)


## Tournaments

tournements/[subpath]

### open_tournement

| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
| Creates a tournament and sends invitation to all players  | POST | 'username', 'password'
			'date_start', 
			'max_players', 
			'cost', 
			'price_1', 
			'price_2',
			'price_3',
			'players':[username1, username2, ...]	 | None |  200 (tournament created), 400 (incorrect data), 404 (user not in database), 500|

### accept_invitation
| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
|Payer accepts the invitation to a turnaament| POST | 'username' 'password' 'tournement_id' | None |  200 (invitation accepted), 400 (incorrect data), 404 (user not in database), 500|

### close tournament (to start tournament)
| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
|Payer accepts the invitation to a turnaament| POST | 'username' 'password' 'tournement_id' | None |  200 (invitation accepted), 400 (incorrect data), 404 (user not in database), 500|

### start match
| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
|When the first player access to the match| POST | 'username' 'password' 'tournement_id' | None |  200 (invitation accepted), 400 (incorrect data), 404 (user not in database), 500|

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
