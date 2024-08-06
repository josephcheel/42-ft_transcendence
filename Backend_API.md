# Table of contents
[create_user/](#create_user/)

## create_user/


Creates User if not in the database.

Methods: POST

Body: {username, password}

returns: 201, 409 (already exists), 400, 500