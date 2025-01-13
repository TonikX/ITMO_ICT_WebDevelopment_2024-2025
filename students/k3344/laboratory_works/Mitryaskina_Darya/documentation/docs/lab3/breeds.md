# Породы (Breed)
---
## Получение списка пород

URL: `/breeds/`  
Метод: `GET`    
Права доступа: `Аутентифицированный пользователь`    

Пример запроса:

```
GET /breeds/
Authorization: Bearer <ваш токен>
```

Пример ответа:

```json
[
    {
        "id": 1,
        "name": "Leghorn",
        "avg_eggs_per_month": 25,
        "avg_weight": 1800,
        "diet": 1
    },
    {
        "id": 2,
        "name": "Rhode Island Red",
        "avg_eggs_per_month": 20,
        "avg_weight": 2000,
        "diet": 2
    }
]
```

---
## Создание породы

URL: `/breeds/create/`  
Метод: `POST`    
Права доступа: `Администратор или менеджер`    

Пример запроса:

```
POST /breeds/create/
Authorization: Bearer <ваш токен>
Content-Type: application/json

{
    "name": "Plymouth Rock",
    "avg_eggs_per_month": 22,
    "avg_weight": 2200,
    "diet": 1
}
```

Пример ответа:

```json
{
    "id": 3,
    "name": "Plymouth Rock",
    "avg_eggs_per_month": 22,
    "avg_weight": 2200,
    "diet": 1
}

```

---
## Обновление породы

URL: `/breeds/<id>/update/`  
Метод: `PUT`    
Права доступа: `Администратор или менеджер`    

Пример запроса:

```
PUT /breeds/1/update/
Authorization: Bearer <ваш токен>
Content-Type: application/json

{
    "avg_eggs_per_month": 26
}
```

Пример ответа:

```json
{
    "id": 1,
    "name": "Leghorn",
    "avg_eggs_per_month": 26,
    "avg_weight": 1800,
    "diet": 1
}
```

---
## Удаление породы

URL: `/breeds/<id>/delete/`  
Метод: `DELETE`    
Права доступа: `Администратор или менеджер`    

Пример запроса:

```
DELETE /breeds/2/delete/
Authorization: Bearer <ваш токен>
```

Пример ответа:

```json
{
    "message": "Breed with ID 2 was successfully deleted."
}
```
---
