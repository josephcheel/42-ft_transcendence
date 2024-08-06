# Table of contents
[create_user/](#create_user/)


All API calls will return a json response and the corresponding code

json response format:

{
    'status' : 'error' / 'success',
    'message' : A short message,
    'data' : None / 'Data'

}

## create_user/

Creates User if not in the database.

Methods: POST
Request data = {username, password}

Response data: {id, username (same as in request data)}

returns: 201, 409 (already exists), 400, 500