# Список всех копий книг

Позволяет посмотреть список всех копий книг

***URL*** : `/library/book-copy`

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
            "cipher": "35",
            "publishing_year": 2020,
            "book": 1
        },
        {
            "id": 2,
            "cipher": "12",
            "publishing_year": 2019,
            "book": 1
        },
        {
            "id": 3,
            "cipher": "13",
            "publishing_year": 2019,
            "book": 2
        },
        {
            "id": 4,
            "cipher": "14",
            "publishing_year": 2019,
            "book": 2
        },
        {
            "id": 5,
            "cipher": "15",
            "publishing_year": 2020,
            "book": 2
        }
    ]