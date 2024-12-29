# Warriors and Skills

**Эндпоинт:** `GET /warriors-with-skills/`

Возвращает список всех войнов с их навыками.

**Пример запроса:**
```bash
GET /warriors/skills/
```

**Пример ответа:**
```js
[
    {
        "id": 1,
        "name": "Arthur",
        "level": 5,
        "race": "s",
        "skill": [
            { "title": "Sword Fighting" },
            { "title": "Shield Defense" }
        ]
    }
]

```
