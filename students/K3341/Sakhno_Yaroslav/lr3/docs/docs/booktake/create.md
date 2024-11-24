# Добавление новой копии книги

Позволяет добавить новую копию книги 

***URL*** : `/library/book-taken`

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
        "take_date": "2024-01-04",
        "return_date": "2024-02-04",
        "book_copy": 6,
        "reader": 2
    }