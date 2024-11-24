# Информация об авторе

Позволяет посмотреть информацию об авторе

***URL*** : `/library/author/pk`

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
        "full_name": "Фет А.А."
    }