#!/bin/sh
echo "Running tests"
echo "Create user"
curl -c cookies1.txt -X POST  http://usermanagement:8000/user/create_user     -H "Content-Type: application/json"      -d '{"username": "test1", "password": "test","first_name":"aaa", "last_name":"bbb"}' -d '{"username": "test1", "password": "test1","first_name":"aaa", "last_name":"}'

echo "Login"

curl -o cookies1.txt -X POST  http://usermanagement:8000/user/login_user     -H "Content-Type: application/json"      -d '{"username": "test1", "password": "test"}'

echo "list users"

curl -o cookies1.txt -X GET  http://usermanagement:8000/user/list_users     -H "Content-Type: application/json"      -d '{"username": "test", "password": "test"}'
