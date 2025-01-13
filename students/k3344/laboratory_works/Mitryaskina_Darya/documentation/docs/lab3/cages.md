# Клетки (Cage)

---

## Получение списка клеток

URL: `/cages/`  
Метод: `GET`    
Права доступа: `Аутентифицированный пользователь`    

Пример запроса:

```
GET /cages/
Authorization: Bearer <ваш токен>
```

Пример ответа:

```json
[
    {
        "id": 1,
        "workshop": 1,
        "row_number": 1,
        "cage_number": 1
    },
    {
        "id": 2,
        "workshop": 1,
        "row_number": 1,
        "cage_number": 2
    }
]
```

---
## Создание клетки

URL: `/cages/create/`  
Метод: `POST`    
Права доступа: `Администратор или менеджер`    

Пример запроса:

```
POST /cages/create/
Authorization: Bearer <ваш токен>
Content-Type: application/json

{
    "workshop": 1,
    "row_number": 2,
    "cage_number": 3
}
```

Пример ответа:

```json
{
    "id": 3,
    "workshop": 1,
    "row_number": 2,
    "cage_number": 3
}
```

---
## Обновление клетки

URL: `/cages/<id>/update/`  
Метод: `PUT`    
Права доступа: `Администратор или менеджер`    

Пример запроса:

```
PUT /cages/1/update/
Authorization: Bearer <ваш токен>
Content-Type: application/json

{
    "row_number": 2,
    "cage_number": 4
}
```

Пример ответа:

```json
{
    "id": 1,
    "workshop": 1,
    "row_number": 2,
    "cage_number": 4
}
```

---
## Удаление клетки

URL: `/cages/<id>/delete/`  
Метод: `DELETE`    
Права доступа: `Администратор или менеджер`    

Пример запроса:

```
DELETE /cages/1/delete/
Authorization: Bearer <ваш токен>
```

Пример ответа:

```json
{
    "message": "Cage with ID 1 was successfully deleted."
}
```
---
