# Добавление нового читального зала

Позволяет добавить новый читальный зал

***URL*** : `/library/reading-room`

***Method*** : `POST`

***Auth required*** : YES

***Permission required*** : None

## Success Responses

HTTP 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 5,
    "name": "Зал №3",
    "capacity": 15
}