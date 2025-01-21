# Получить список всех навыков

Возвращает список всех доступных навыков.

**URL** : `/api/skills/`

**Method** : `GET`

**Auth required** : YES

**Permissions required** : None

**Data constraints** : `{}`

## Success Responses

**Code** : `200 OK`

**Content** : `[{...}]`

```json
{
    "Skills": [
        {
            "id": 1,
            "title": "Swordsmanship"
        },
        {
            "id": 2,
            "title": "Archery"
        }
    ]
}
```

# Создать новый навык

Создает новый навык.

**URL** : `/api/skills/`

**Method** : `POST`

**Auth required** : YES

**Permissions required** : None

**Data constraints** : `{}`

## Data

```json
{
    "skill": {
        "title": "string"
    }
}
```

## Success Responses

**Code** : `201 Created`

**Content** : `[{...}]`

```json
{
    "Success": "Skill 'Archery' created successfully."
}
```