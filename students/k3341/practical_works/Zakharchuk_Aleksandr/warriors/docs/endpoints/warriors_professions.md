# Warriors and Professions

**Эндпоинт:** `GET /warriors-with-professions/`

Возвращает список всех войнов с их профессиями.

**Пример запроса:**
```bash
GET /warriors/professions/
```

**Пример ответа:**
```js
[
    {
        "id": 1,
        "name": "Arthur",
        "level": 5,
        "race": "s",
        "profession": {
            "title": "Knight",
            "description": "Protects the realm"
        }
    }
]

```
