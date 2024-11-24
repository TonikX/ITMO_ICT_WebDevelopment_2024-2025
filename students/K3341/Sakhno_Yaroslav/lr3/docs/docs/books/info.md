# Информация о книге

Позволяет посмотреть информацию о книге

***URL*** : `/library/book/pk`

***Method*** : `GET`

***Auth required*** : YES

***Permission required*** : None

## Success Responses

    HTTP 200 OK
    Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept
    
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