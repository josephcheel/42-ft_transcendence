# Table of contents
## [User](#User)
[create_user/](#create_user/)
[login_user/](#login_user/)
[is_logged_in/](#is_logged_in/)


All API calls will return a json response and the corresponding code

json response format:

{
    'status' : 'error' / 'success',
    'message' : A short message,
    'data' : None / 'Data'

}
## User

Uses user/[subpath]

### create_user/

| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
| Creates User if not in the database. | POST | {username, password} | {user id, username (same as in request data)} |  201, 409 (already exists), 400, 500 |


### login_user/

| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
| Logs in User| POST | username, password | user is loged in message |200, 400, 401 (invalid credentials), 500|


### is_logged_in/

| Use | Methods | Request Data | Response Data | Return Values|
| --- | --- | --- | ---| ---|
| Checks if user is logged in | GET | username | User is logged in message |  200 (user logged in), 400, 404 (user not logged in), 500|