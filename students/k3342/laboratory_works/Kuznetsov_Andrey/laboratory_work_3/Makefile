USERNAME ?= your_username
PASSWORD ?= your_password
EMAIL ?= your_email
TOKEN ?= your_token
REFRESH_TOKEN ?= your_refresh_token

login:
	curl -X POST -d "username=$(USERNAME)&password=$(PASSWORD)&email=$(EMAIL)" http://localhost:8000/auth/users/

get-token:
	curl -X POST -d "username=${USERNAME}&password=${PASSWORD}" http://localhost:8000/api/token/

refresh-token:
	curl -X POST -d "refresh=${REFRESH_TOKEN}" http://localhost:8000/api/token/refresh/