# Warrior details

**Эндпоинт:** `GET /warrior/<id>/`

Возвращает подробную информацию о конкретном войне, включая его профессию и навыки.

**Пример запроса**
```bash
GET /warriors/1/
```

**Пример ответа**
```js
{
    "id": 1,
    "name": "Arthur",
    "level": 5,
    "race": "s",
    "profession": {
        "title": "Knight",
        "description": "Protects the realm"
    },
    "skill": [
        {
            "title": "Sword Fighting"
        },
        {
            "title": "Shield Defense"
        }
    ]
}
```
