# Список всех читателей

Позволяет посмотреть список всех читателей

***URL*** : `/library/reader`

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
            "full_name": "Галибов М.О.",
            "passport": "1234123456",
            "birth_date": "2003-03-11",
            "phone_number": "+79939614888",
            "education": "н",
            "degree": false,
            "registration_date": "2024-01-06",
            "reading_ticket": 1223,
            "reading_room": 1
        },
        {
            "id": 2,
            "full_name": "Соколовская А.В.",
            "passport": "2441130",
            "birth_date": "2003-09-13",
            "phone_number": "+79819068181",
            "education": "н",
            "degree": false,
            "registration_date": "2024-01-06",
            "reading_ticket": 1124,
            "reading_room": 1
        },
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
    ]