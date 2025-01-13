# Куры (Hen)
---
## Получение списка кур

URL: `/hens/`  
Метод: `GET`    
Права доступа: `Аутентифицированный пользователь`    

Пример запроса:

```
GET /hens/
Authorization: Bearer <ваш токен>
```

Пример ответа:

```json
[
    {
        "id": 1,
        "weight": 1700,
        "age": 12,
        "eggs_per_month": 24,
        "breed": 1,
        "cage": 1
    },
    {
        "id": 2,
        "weight": 2000,
        "age": 18,
        "eggs_per_month": 22,
        "breed": 2,
        "cage": 2
    }
]
```

---
## Создание курицы

URL: `/hens/create/`  
Метод: `POST`    
Права доступа: `Администратор или менеджер`    

Пример запроса:

```
POST /hens/create/
Authorization: Bearer <ваш токен>
Content-Type: application/json

{
    "weight": 1850,
    "age": 10,
    "eggs_per_month": 23,
    "breed": 1,
    "cage": 1
}
```

Пример ответа:

```json
{
    "id": 3,
    "weight": 1850,
    "age": 10,
    "eggs_per_month": 23,
    "breed": 1,
    "cage": 1
}
```

---
## Обновление курицы

URL: `/hens/<id>/update/`  
Метод: `PUT`    
Права доступа: `Администратор или менеджер`    

Пример запроса:

```
PUT /hens/1/update/
Authorization: Bearer <ваш токен>
Content-Type: application/json

{
    "weight": 1750,
    "cage": 2
}
```

Пример ответа:

```json
{
    "id": 1,
    "weight": 1750,
    "age": 12,
    "eggs_per_month": 24,
    "breed": 1,
    "cage": 2
}
```

---
## Удаление курицы

URL: `/hens/<id>/delete/`  
Метод: `DELETE`    
Права доступа: `Администратор или менеджер`    

Пример запроса:

```
DELETE /hens/1/delete/
Authorization: Bearer <ваш токен>
```

Пример ответа:

```json
{
    "message": "Hen with ID 1 was successfully deleted."
}
```
---
