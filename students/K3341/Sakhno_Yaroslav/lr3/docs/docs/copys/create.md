# Добавление новой копии книги

Позволяет добавить новую копию книги

***URL*** : `/library/book-copy`

***Method*** : `POST`

***Auth required*** : YES

***Permission required*** : None

## Success Responses

    HTTP 201 Created
    Allow: GET, POST, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept
    
    {
        "id": 6,
        "cipher": "565",
        "publishing_year": 2017,
        "book": 3
    }