# Добавление новой книги

Позволяет добавить новую книгу 

***URL*** : `/library/book`

***Method*** : `POST`

***Auth required*** : YES

***Permission required*** : None

## Success Responses

    HTTP 201 Created
    Allow: GET, POST, HEAD, OPTIONS
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