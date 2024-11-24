# Добавление автора

Позволяет добавить нового автора

***URL*** : `/library/author`

***Method*** : `POST`

***Auth required*** : YES

***Permission required*** : None

## Success Responses

    HTTP 201 Created
    Allow: GET, POST, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept
    
    {
        "id": 4,
        "full_name": "Фет А.А."
    }