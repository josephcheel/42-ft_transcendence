# Table of contents
| Section | Links |
|---------|-------|
| [User](#user) | [create_user](#create_user) <br> [login_user](#login_user) <br> [logout_user](#logout_user) <br> [is_logged_in](#is_logged_in) <br> [list_users](#list_users) <br> [user_status](#user_status) |
| [Match](#match) | [propose_match](#propose_match) <br> [get_pending_matches](#get_pending_matches) |


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
| Checks if YOUR user is logged in | GET | None | None |  200 (user logged in), 401 (Unauthorized), 405, 500|

### list_users

| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
| Returns a list of all users registered | GET | None | List of users. Each element inside the list is a dictionaty with id and username keys |  200 (user logged in), 405, 500|

### user_status

| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
| Returns current online status of user | GET | username | is_online: True/False |  200 (user logged in), 404 (user not found), 405, 500|


[Back to Top](#table-of-contents)


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
