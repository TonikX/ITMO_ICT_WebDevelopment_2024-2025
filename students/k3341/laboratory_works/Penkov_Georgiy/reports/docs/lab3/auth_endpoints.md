
## Аутентификация

### Регистрация (POST /auth/users/)

Создает нового пользователя.

**Пример запроса:**

```http
POST /auth/users/
Content-Type: application/json

{
  "username": "^w$",
  "password": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "phone_number": "string",
  "city": 0
}
```

**Пример ответа:**

```json
{
  "username": "^w$",
  "password": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "phone_number": "string",
  "city": 0
}
```

### Авторизация (POST /auth/token/login/)

Получение токена для аутентификации.

**Пример запроса:**

```http
POST /auth/token/login/
Content-Type: application/json

{
  "password": "string",
  "username": "string"
}
```

**Пример ответа:**

```json
{
  "auth_token": "your-token-here"
}
```

### Изменение учетных данных (PATCH /auth/users/{id}/)

Обновляет данные пользователя.

**Пример запроса:**

```http
PATCH /auth/users/2/
Authorization: Token your-token-here
Content-Type: application/json

{
  "username": "^w$",
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "is_superuser": true,
  "is_staff": true,
  "phone_number": "string",
  "city": 0
}
```

**Пример ответа:**

```json
{
  "id": 0,
  "username": "^w$",
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "is_superuser": true,
  "is_staff": true,
  "phone_number": "string",
  "city": 0,
  "club": {
    "id": 0,
    "name": "string",
    "country": 0,
    "city": 0,
    "contact_user": 0
  }
}
```