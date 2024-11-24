# Информация о читальном зале

Позволяет посмотреть информацию о читальном зале

***URL*** : `/library/reading-room/pk`

***Method*** : `GET`

***Auth required*** : YES

***Permission required*** : None

## Success Responses

HTTP 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 5,
    "name": "Зал №3",
    "capacity": 15
}