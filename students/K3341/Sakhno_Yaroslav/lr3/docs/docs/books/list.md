# Список всех книг

Позволяет посмотреть список всех книг

***URL*** : `/library/category`

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
            "name": "Белые ночи",
            "publisher": "МИФ",
            "category": [
                4,
                5
            ],
            "authors": [
                1
            ]
        },
        {
            "id": 2,
            "name": "Отцы и дети",
            "publisher": "МИФ",
            "category": [
                3
            ],
            "authors": [
                3
            ]
        },
        {
            "id": 3,
            "name": "Мастер и Маргарита",
            "publisher": "МИФ",
            "category": [
                3
            ],
            "authors": [
                2
            ]
        }
    ]