# Информация о копии книги

Позволяет посмотреть информацию о копии книги

***URL*** : `/library/book-copy`

***Method*** : `GET`

***Auth required*** : YES

***Permission required*** : None

## Success Responses

    HTTP 200 OK
    Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept
    
    {
        "id": 6,
        "cipher": "565",
        "publishing_year": 2017,
        "book": 3
    }