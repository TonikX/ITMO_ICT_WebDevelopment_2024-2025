# Printing House - Go REST API

## Описание

Printing House это REST API на Go для системы управления типографией, газетами и их распределением. Реализовано с использованием чистой архитектуры и современных практик разработки на Go.

## Архитектура

Проект следует принципам **Clean Architecture**:

```
internal/
├── entities/       # Доменные модели
├── cases/          # Бизнес-логика (use cases)
├── adapters/       # Реализации (PostgreSQL)
└── ports/          # Внешние интерфейсы (HTTP)
```

## Модели данных (Entities)

### Newspaper
Модель газеты:

```go
type Newspaper struct {
    ID               int     `json:"id"`
    Title            string  `json:"title"`                // Название газеты
    PublicationIndex string  `json:"publication_index"`    // Индекс издания
    EditorFirstName  string  `json:"editor_first_name"`    // Имя редактора
    EditorLastName   string  `json:"editor_last_name"`     // Фамилия редактора
    EditorMiddleName *string `json:"editor_middle_name"`   // Отчество редактора
    PricePerCopy     float64 `json:"price_per_copy"`       // Цена за копию
}
```

### PrintingHouse
Модель типографии:

```go
type PrintingHouse struct {
    ID       int    `json:"id"`
    Name     string `json:"name"`        // Название
    Address  string `json:"address"`     // Адрес
    IsActive bool   `json:"is_active"`   // Активна ли
}
```

### PostOffice
Модель почтового отделения:

```go
type PostOffice struct {
    ID      int    `json:"id"`
    Number  string `json:"number"`   // Номер отделения (уникальный)
    Address string `json:"address"`  // Адрес отделения
}
```

### PrintingRun
Тираж газеты (связь между типографией и газетой):

```go
type PrintingRun struct {
    ID              int `json:"id"`
    PrintingHouseID int `json:"printing_house_id"`  // ID типографии
    NewspaperID     int `json:"newspaper_id"`       // ID газеты
    Circulation     int `json:"circulation"`        // Объём тиража
}
```

### Distribution
Распределение газет почтовым отделениям:

```go
type Distribution struct {
    ID              int `json:"id"`
    PostOfficeID    int `json:"post_office_id"`     // ID почтового отделения
    NewspaperID     int `json:"newspaper_id"`       // ID газеты
    PrintingHouseID int `json:"printing_house_id"`  // ID типографии
    Quantity        int `json:"quantity"`           // Количество экземпляров
}
```

### User
Пользователь системы:

```go
type User struct {
    ID           int       `json:"id"`
    Username     string    `json:"username"`
    Email        string    `json:"email"`
    PasswordHash string    `json:"-"`  // Не возвращается в JSON
    CreatedAt    time.Time `json:"created_at"`
}
```

### APIToken
JWT токен для аутентификации:

```go
type APIToken struct {
    ID        int       `json:"id"`
    UserID    int       `json:"user_id"`
    Token     string    `json:"token"`
    ExpiresAt time.Time `json:"expires_at"`
    CreatedAt time.Time `json:"created_at"`
}
```

## API Endpoints

**Base URL:** `http://localhost:8080/api/v1`

**Аутентификация:** JWT Bearer Token в заголовке `Authorization: Bearer <token>`

### Authentication API

#### Регистрация
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "username": "newuser",
  "email": "user@example.com",
  "password": "password123"
}
```

Ответ:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "newuser",
    "email": "user@example.com",
    "created_at": "2026-02-17T00:00:00Z"
  }
}
```

#### Вход
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "newuser",
  "password": "password123"
}
```

Ответ аналогичен регистрации.

#### Получить текущего пользователя
```http
GET /api/v1/auth/me
Authorization: Bearer <token>
```

### Newspapers API

#### Список газет
```http
GET /api/v1/newspapers
Authorization: Bearer <token>
```

Ответ:
```json
[
  {
    "id": 1,
    "title": "Pravda",
    "publication_index": "2312-3652",
    "editor_first_name": "Ivan",
    "editor_last_name": "Petrov",
    "editor_middle_name": "Ivanovich",
    "price_per_copy": 15.50
  }
]
```

#### Создать газету
```http
POST /api/v1/newspapers
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Izvestiya",
  "publication_index": "2312-3653",
  "editor_first_name": "Pavel",
  "editor_last_name": "Ivanov",
  "price_per_copy": 18.50
}
```

#### Получить/обновить/удалить газету
```http
GET /api/v1/newspapers/{id}
PUT /api/v1/newspapers/{id}
DELETE /api/v1/newspapers/{id}
Authorization: Bearer <token>
```

### Printing Houses API

#### Список типографий
```http
GET /api/v1/printing-houses
Authorization: Bearer <token>
```

#### Создать типографию
```http
POST /api/v1/printing-houses
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "PrintCo Moscow",
  "address": "Moscow, Tverskaya str. 10",
  "is_active": true
}
```

### Post Offices API

#### Список отделений
```http
GET /api/v1/post-offices
Authorization: Bearer <token>
```

#### Создать отделение
```http
POST /api/v1/post-offices
Authorization: Bearer <token>
Content-Type: application/json

{
  "number": "101000",
  "address": "Moscow, center"
}
```

### Distributions API

#### Список распределений
```http
GET /api/v1/distributions
Authorization: Bearer <token>
```

#### Создать распределение
```http
POST /api/v1/distributions
Authorization: Bearer <token>
Content-Type: application/json

{
  "post_office_id": 1,
  "newspaper_id": 1,
  "printing_house_id": 1,
  "quantity": 5000
}
```

## Workflow

1. Зарегистрироваться или войти в систему (получить JWT токен)
2. Создать газету
3. Создать типографию
4. Создать почтовое отделение
5. Создать распределение (связывает всё вместе)

## Примеры (curl)

```bash
# 1. Регистрация
curl -X POST http://localhost:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'

# Сохранить токен из ответа
TOKEN="<your_jwt_token>"

# 2. Получить список газет
curl http://localhost:8080/api/v1/newspapers \
  -H "Authorization: Bearer $TOKEN"

# 3. Создать газету
curl -X POST http://localhost:8080/api/v1/newspapers \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Daily News",
    "publication_index": "2312-1111",
    "editor_first_name": "John",
    "editor_last_name": "Smith",
    "price_per_copy": 20.00
  }'

# 4. Создать типографию
curl -X POST http://localhost:8080/api/v1/printing-houses \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Moscow Print",
    "address": "Moscow, Red Square",
    "is_active": true
  }'

# 5. Создать распределение
curl -X POST http://localhost:8080/api/v1/distributions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "post_office_id": 1,
    "newspaper_id": 1,
    "printing_house_id": 1,
    "quantity": 5000
  }'
```

## HTTP методы

| Метод | Эндпоинт | Действие | Auth |
|-------|----------|---------|------|
| POST | /api/v1/auth/register | Регистрация | Нет |
| POST | /api/v1/auth/login | Вход | Нет |
| GET | /api/v1/auth/me | Текущий пользователь | JWT |
| GET | /api/v1/newspapers | Список газет | JWT |
| POST | /api/v1/newspapers | Создать газету | JWT |
| GET | /api/v1/printing-houses | Список типографий | JWT |
| POST | /api/v1/printing-houses | Создать типографию | JWT |
| GET | /api/v1/post-offices | Список отделений | JWT |
| POST | /api/v1/post-offices | Создать отделение | JWT |
| GET | /api/v1/distributions | Список распределений | JWT |
| POST | /api/v1/distributions | Создать распределение | JWT |

## Технические особенности

- **Чистая архитектура** - разделение на слои (entities, use cases, adapters, ports)
- **Dependency Injection** - внедрение зависимостей через конструкторы
- **Repository Pattern** - абстракция работы с БД
- **JWT аутентификация** - токены со сроком действия 7 дней
- **Bcrypt** - хеширование паролей
- **PostgreSQL** - реляционная БД с миграциями
- **Docker** - контейнеризация приложения и БД

Дополнительно: [Вернуться к обзору Lr3](index.md)
