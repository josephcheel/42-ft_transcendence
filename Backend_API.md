# Table of contents
## [User](#user)
[create_user/](#create_user)
[login_user/](#login_user)
[is_logged_in/](#is_logged_in)

## [Match](#match)
[propose_match/](#propose_match)
[get_pending_matches/](#get_pending_matches)

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
| Creates User if not in the database. | POST | {username, password} | {user id, username (same as in request data)} |  201, 409 (already exists), 400, 500 |


### login_user

| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
| Logs in User| POST | username, password | None |200, 400, 401 (invalid credentials), 500|


### is_logged_in

| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
| Checks if user is logged in | GET | username | None |  200 (user logged in), 400, 404 (user not logged in), 500|


## Match

match/[subpath]

### propose_match

| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
| Sends invitation to all players | POST | start_time, players[first player is the owner/creator] | None |  200 (user logged in), 400, 404 (user not in database), 500|

### get_pending_matches

| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
| Checks if user has pending matches to accept | GET | player (in query) | List of pending invitations or empty list |  200 , 400, 404 (user not in database), 500|