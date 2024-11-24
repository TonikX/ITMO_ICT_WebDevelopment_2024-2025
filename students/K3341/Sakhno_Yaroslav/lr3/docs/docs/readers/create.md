# Добавление нового читателя

Позволяет добавить нового читателя

***URL*** : `/library/reader`

***Method*** : `POST`

***Auth required*** : YES

***Permission required*** : None

## Success Responses

    HTTP 201 Created
    Allow: GET, POST, HEAD, OPTIONS
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