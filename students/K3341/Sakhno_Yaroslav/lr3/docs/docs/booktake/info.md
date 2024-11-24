# Информация о копии книги

Позволяет посмотреть информацию о копии книги

***URL*** : `/library/book-taken`

***Method*** : `GET`

***Auth required*** : YES

***Permission required*** : None

## Success Responses
    HTTP 200 OK
    Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept
    
    {
        "id": 4,
        "take_date": "2024-01-06",
        "return_date": "2024-02-06",
        "book_copy": 1,
        "reader": 1
    }