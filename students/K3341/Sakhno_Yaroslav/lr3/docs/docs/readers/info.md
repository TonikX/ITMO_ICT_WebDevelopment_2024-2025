# Информация о читателе

Позволяет посмотреть информацию о читателе

***URL*** : `/library/reader/pk`

***Method*** : `GET`

***Auth required*** : YES

***Permission required*** : None

## Success Responses

    HTTP 200 OK
    Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept
    
    {
        "id": 3,
        "full_name": "Пронина Мария Владимировна",
        "passport": "1436228",
        "birth_date": "2003-10-27",
        "phone_number": "79819057474",
        "education": "с",
        "degree": false,
        "registration_date": "2024-01-08",
        "reading_ticket": 5,
        "reading_room": 4
    }