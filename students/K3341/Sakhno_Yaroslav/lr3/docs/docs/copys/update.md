# Изменение информации о копии книги

Позволяет изменить информацию о копии книги

***URL*** : `/library/book-copy/pk`

***Method*** : `PATCH`

***Auth required*** : YES

***Permission required*** : None

## Success Responses

    HTTP 200 OK
    Allow: GET, POST, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept
    
    
    {
        "id": 6,
        "cipher": "587",
        "publishing_year": 2017,
        "book": 3
    }