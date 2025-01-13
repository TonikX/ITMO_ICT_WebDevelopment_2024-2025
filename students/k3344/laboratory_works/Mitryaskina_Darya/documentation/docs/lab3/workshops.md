# Цеха (Workshop)

---

## Получение списка цехов

URL: `/workshops/`  
Метод: `GET`    
Права доступа: `Аутентифицированный пользователь`    

Пример запроса:

```
GET /workshops/
Authorization: Bearer <ваш токен>
```

Пример ответа:

```json
[
    {
        "id": 1,
        "info": "Workshop for egg production",
        "rows": 3
    },
    {
        "id": 2,
        "info": "Workshop for broilers",
        "rows": 2
    }
]
```

---
## Создание цеха

URL: `/workshops/create/`  
Метод: `POST`    
Права доступа: `Администратор или менеджер`    

Пример запроса:

```
POST /workshops/create/
Authorization: Bearer <ваш токен>
Content-Type: application/json

{
    "info": "Workshop for chicks",
    "rows": 4
}
```

Пример ответа:

```json
{
    "id": 3,
    "info": "Workshop for chicks",
    "rows": 4
}
```

---
## Обновление цеха

URL: `/workshops/<id>/update/`  
Метод: `PUT`    
Права доступа: `Администратор или менеджер`    

Пример запроса:

```
PUT /workshops/1/update/
Authorization: Bearer <ваш токен>
Content-Type: application/json

{
    "info": "Updated workshop for egg production",
    "rows": 5
}
```

Пример ответа:

```json
{
    "id": 1,
    "info": "Updated workshop for egg production",
    "rows": 5
}
```

---
## Удаление цеха

URL: `/workshops/<id>/delete/`  
Метод: `DELETE`    
Права доступа: `Администратор или менеджер`    

Пример запроса:

```
DELETE /workshops/1/delete/
Authorization: Bearer <ваш токен>
```

Пример ответа:

```json
{
    "message": "Workshop with ID 1 was successfully deleted."
}
```
---
