# Диеты (Diet)   
---
## Получение списка диет

URL: `/diets/`  
Метод: `GET`    
Права доступа: `Аутентифицированный пользователь`    

Пример запроса:

```
GET /diets/
Authorization: Bearer <ваш токен>
```

Пример ответа:

```json
[
    {
        "id": 1,
        "season": "SPRING",
        "composition": "Corn, wheat, vitamins"
    },
    {
        "id": 2,
        "season": "SUMMER",
        "composition": "Barley, soy, minerals"
    }
]
```
---
## Создание диеты

URL: `/diets/create/`  
Метод: `POST`    
Права доступа: `Администратор или менеджер`    

Пример запроса:

```
POST /diets/create/
Authorization: Bearer <ваш токен>
Content-Type: application/json

{
    "season": "AUTUMN",
    "composition": "Oats, protein supplements, calcium"
}
```

Пример ответа:

```json
{
    "id": 3,
    "season": "AUTUMN",
    "composition": "Oats, protein supplements, calcium"
}
```
---

## Обновление диеты

URL: `/diets/<id>/update/`  
Метод: `PUT`    
Права доступа: `Администратор или менеджер`    

Пример запроса:

```
PUT /diets/1/update/
Authorization: Bearer <ваш токен>
Content-Type: application/json

{
    "season": "WINTER",
    "composition": "Wheat, corn, high-protein supplements"
}
```

Пример ответа:

```json
{
    "id": 1,
    "season": "WINTER",
    "composition": "Wheat, corn, high-protein supplements"
}
```

---

## Удаление диеты

URL: `/diets/<id>/delete/`  
Метод: `DELETE`    
Права доступа: `Администратор или менеджер`    

Пример запроса:

```
DELETE /diets/1/delete/
Authorization: Bearer <ваш токен>
```

Пример ответа:

```json
{
    "message": "Diet with ID 1 was successfully deleted."
}
```
