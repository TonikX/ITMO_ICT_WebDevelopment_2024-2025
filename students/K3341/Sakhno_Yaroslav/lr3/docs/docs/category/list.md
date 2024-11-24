# Список всех категорий

Позволяет посмотреть список всех категорий

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
            "category_name": "Классика"
        },
        {
            "id": 3,
            "category_name": "Роман"
        },
        {
            "id": 4,
            "category_name": "Фикшн"
        },
        {
            "id": 5,
            "category_name": "Повесть"
        },
        {
            "id": 6,
            "category_name": "Фантастика"
        }
    ]
