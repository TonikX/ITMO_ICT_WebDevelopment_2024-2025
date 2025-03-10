USERNAME=doodoo
PASSWORD=QWERTY1234!
EMAIL=dodo@gmail.com
REPASSWORD=QWERTY1234!
TOKEN=92e5cacd2969be00b964e1f93b76b7e8a57f93b0

curl -X POST -d "username=$USERNAME&password=$PASSWORD&email=$EMAIL&re_password=$REPASSWORD" http://localhost:8000/auth/users/
curl -X POST -d "username=${USERNAME}&password=${PASSWORD}" http://localhost:8000/auth/token/login
curl -H "Authorization: Token $TOKEN" http://localhost:8000/api/v1/blogs/

echo "\n"