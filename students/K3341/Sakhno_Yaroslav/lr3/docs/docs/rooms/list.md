# Список всех читальных залов

Позволяет посмотреть список всех читальных залов

***URL*** : `/library/reading-room`

***Method*** : `GET`

***Auth required*** : YES

***Permission required*** : None

## Success Responses

HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "id": 1,
        "name": "Главный зал",
        "capacity": 24
    },
    {
        "id": 2,
        "name": "Малый зал",
        "capacity": 5
    },
    {
        "id": 3,
        "name": "Зал №1",
        "capacity": 10
    },
    {
        "id": 4,
        "name": "Зал №2",
        "capacity": 10
    }
]