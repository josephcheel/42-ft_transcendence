#!/bin/sh
echo "Running tests"
echo "Create user"
curl -X POST  http://usermanagement:8000/user/create_user     -H "Content-Type: application/json"      -d '{"username": "test", "password": "test","first_name":"aaa", "last_name":"bbb"}' -d '{"username": "test", "password": "test","first_name":"aaa", "last_name":"}'

echo "Login"

curl -X POST  http://usermanagement:8000/user/login_user     -H "Content-Type: application/json"      -d '{"username": "test", "password": "test"}'

echo "list users"

curl -X GET  http://usermanagement:8000/user/list_users     -H "Content-Type: application/json"      -d '{"username": "test", "password": "test"}'
