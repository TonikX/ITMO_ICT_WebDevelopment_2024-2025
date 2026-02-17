# Printing House API (Lr4 - Go Backend)

## Описание

Printing House приложение на Go управляет газетами, типографиями и их распределением. Это серверная часть Full Stack приложения с чистой архитектурой.

## Архитектура

Проект построен с использованием **Clean Architecture**:

```
printing_house_go/
├── internal/
│   ├── entities/       # Доменные модели
│   ├── cases/          # Бизнес-логика (use cases)
│   ├── adapters/       # Адаптеры (PostgreSQL)
│   └── ports/          # Внешние интерфейсы (HTTP)
├── pkg/
│   └── dto/            # Data Transfer Objects
└── deployment/
    ├── config/         # Конфигурация
    └── migrations/     # SQL миграции
```

## Модели

### Newspaper
```go
type Newspaper struct {
    ID               int     `json:"id"`
    Title            string  `json:"title"`
    PublicationIndex string  `json:"publication_index"`
    EditorFirstName  string  `json:"editor_first_name"`
    EditorLastName   string  `json:"editor_last_name"`
    EditorMiddleName *string `json:"editor_middle_name"`
    PricePerCopy     float64 `json:"price_per_copy"`
}
```

### PrintingHouse
```go
type PrintingHouse struct {
    ID       int    `json:"id"`
    Name     string `json:"name"`
    Address  string `json:"address"`
    IsActive bool   `json:"is_active"`
}
```

### PostOffice
```go
type PostOffice struct {
    ID      int    `json:"id"`
    Number  string `json:"number"`
    Address string `json:"address"`
}
```

### Distribution
```go
type Distribution struct {
    ID              int `json:"id"`
    PostOfficeID    int `json:"post_office_id"`
    NewspaperID     int `json:"newspaper_id"`
    PrintingHouseID int `json:"printing_house_id"`
    Quantity        int `json:"quantity"`
}
```

### User
```go
type User struct {
    ID           int       `json:"id"`
    Username     string    `json:"username"`
    Email        string    `json:"email"`
    PasswordHash string    `json:"-"`
    CreatedAt    time.Time `json:"created_at"`
}
```

## API Endpoints (порт 8080)

**Base URL:** `http://localhost:8080/api/v1`

**Аутентификация:** JWT Bearer Token

```
Authorization: Bearer <your_jwt_token>
```

### Authentication

**Регистрация:**
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "username": "newuser",
  "email": "user@example.com",
  "password": "password123"
}
```

**Вход:**
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "newuser",
  "password": "password123"
}
```

**Ответ:**
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

**Текущий пользователь:**
```http
GET /api/v1/auth/me
Authorization: Bearer <token>
```

### Newspapers

```http
GET /api/v1/newspapers          # список
POST /api/v1/newspapers         # создать
GET /api/v1/newspapers/{id}     # получить
PUT /api/v1/newspapers/{id}     # обновить
DELETE /api/v1/newspapers/{id}  # удалить
```

### Printing Houses

```http
GET /api/v1/printing-houses          # список
POST /api/v1/printing-houses         # создать
GET /api/v1/printing-houses/{id}     # получить
PUT /api/v1/printing-houses/{id}     # обновить
DELETE /api/v1/printing-houses/{id}  # удалить
```

### Post Offices

```http
GET /api/v1/post-offices          # список
POST /api/v1/post-offices         # создать
GET /api/v1/post-offices/{id}     # получить
PUT /api/v1/post-offices/{id}     # обновить
DELETE /api/v1/post-offices/{id}  # удалить
```

### Distributions

```http
GET /api/v1/distributions          # список
POST /api/v1/distributions         # создать
GET /api/v1/distributions/{id}     # получить
PUT /api/v1/distributions/{id}     # обновить
DELETE /api/v1/distributions/{id}  # удалить
```

## Примеры запросов

### Создать газету
```bash
curl -X POST http://localhost:8080/api/v1/newspapers \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Pravda",
    "publication_index": "2312-3652",
    "editor_first_name": "Ivan",
    "editor_last_name": "Petrov",
    "price_per_copy": 15.50
  }'
```

### Создать типографию
```bash
curl -X POST http://localhost:8080/api/v1/printing-houses \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "PrintCo",
    "address": "Moscow, Tverskaya 10",
    "is_active": true
  }'
```

### Создать распределение
```bash
curl -X POST http://localhost:8080/api/v1/distributions \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "post_office_id": 1,
    "newspaper_id": 1,
    "printing_house_id": 1,
    "quantity": 5000
  }'
```

## Workflow

1. Зарегистрироваться или войти (получить JWT токен)
2. Создать газету
3. Создать типографию
4. Создать почтовое отделение
5. Создать распределение

## Технологии

- **Go** 1.23.0
- **Chi Router** - маршрутизация
- **PostgreSQL** - база данных
- **pgx/v4** - драйвер БД
- **JWT** (golang-jwt/jwt/v5) - аутентификация
- **bcrypt** - хеширование паролей
- **Viper** - конфигурация
- **Docker Compose** - оркестрация

## Запуск

```bash
cd printing_house_go
docker-compose up -d
```

API доступен на `http://localhost:8080`

## Тестовые пользователи

| Username | Email | Password |
|----------|-------|----------|
| admin | admin@printinghouse.local | password123 |
| testuser | test@printinghouse.local | password123 |

## Особенности

- **Clean Architecture** - разделение на слои
- **Dependency Injection** - внедрение зависимостей
- **Repository Pattern** - абстракция БД
- **JWT токены** - срок действия 7 дней
- **Миграции** - версионирование схемы БД
- **CORS** - настроен для frontend на порту 5173

Дополнительно: [Вернуться к обзору Lr4](index.md)
