# Получить список всех воинов

Выводит информацию обо всех воинах с их профессиями.

**URL** : `/api/warriors/`

**Method** : `GET`

**Auth required** : YES

**Permissions required** : None

**Data constraints** : `{}`

## Success Responses

**Code** : `200 OK`

**Content** : `[{...}]`

```json
[
    {
        "id": 1,
        "race": "Human",
        "name": "John",
        "level": 5,
        "profession": {
            "id": 1,
            "title": "Knight"
        },
        "skills": [
            {
                "id": 1,
                "title": "Swordsmanship"
            }
        ]
    },
    {
        "id": 2,
        "race": "Elf",
        "name": "Arwen",
        "level": 10,
        "profession": null,
        "skills": []
    }
]
```

# Получить список всех воинов с навыками

Выводит информацию обо всех воинах и их навыках.

**URL** : `/api/warriors/skills/`

**Method** : `GET`

**Auth required** : YES

**Permissions required** : None

**Data constraints** : `{}`

## Success Responses

**Code** : `200 OK`

**Content** : `[{...}]`

```json
[
    {
        "id": 1,
        "race": "Human",
        "name": "John",
        "level": 5,
        "skills": [
            {
                "id": 1,
                "title": "Swordsmanship"
            },
            {
                "id": 2,
                "title": "Shield Defense"
            }
        ]
    },
    {
        "id": 2,
        "race": "Elf",
        "name": "Arwen",
        "level": 10,
        "skills": []
    }
]
```

# Получить, обновить или удалить воина

Получает, обновляет или удаляет воина по ID.

**URL** : `/api/warriors/<id>/`

**Method** : `GET, PUT, DELETE`

**Auth required** : YES

**Permissions required** : None

**Data constraints** : `{}`

## Data (for PUT)
```json
{
    "name": "string",
    "level": "integer",
    "race": "string",
    "profession": {
        "id": "integer"
    }
}
```

## Success Responses

**Code** : `200 OK`

**Content** : `[{...}]`

Data:

### GET
```json
{
    "id": 1,
    "race": "Human",
    "name": "John",
    "level": 5,
    "profession": {
        "id": 1,
        "title": "Knight"
    },
    "skills": [
        {
            "id": 1,
            "title": "Swordsmanship"
        }
    ]
}
```

### PUT
```json
{
    "id": 1,
    "race": "Human",
    "name": "John",
    "level": 6,
    "profession": {
        "id": 1,
        "title": "Knight"
    },
    "skills": []
}
```

### DELETE
Code: ```204 No Content```

```json
{
    "message": "Warrior deleted successfully"
}
```