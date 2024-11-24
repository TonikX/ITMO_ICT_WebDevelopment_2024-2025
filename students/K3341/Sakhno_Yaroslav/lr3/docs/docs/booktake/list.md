# Список всех копий книг

Позволяет посмотреть список всех копий книг

***URL*** : `/library/book-taken`

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
            "id": 4,
            "take_date": "2024-01-06",
            "return_date": "2024-02-06",
            "book_copy": 1,
            "reader": 1
        },
        {
            "id": 5,
            "take_date": "2023-12-10",
            "return_date": "2024-01-12",
            "book_copy": 3,
            "reader": 2
        }
    ]