# Lr3 - Go REST API Backend

## Описание

Третья лабораторная работа посвящена разработке REST API с использованием Go. Реализован backend для системы управления типографией с чистой архитектурой.

## Цели работы

- Изучить разработку REST API на Go
- Применить чистую архитектуру (Clean Architecture)
- Реализовать JWT аутентификацию
- Работать с PostgreSQL через pgx
- Использовать Chi Router для HTTP маршрутизации
- Контейнеризация с Docker и Docker Compose

## Структура проекта

```
Lr3/
├── printing_house_go/           # Go Backend
│   ├── cmd/                     # Точки входа приложения
│   │   └── main.go              # Главный файл запуска
│   ├── internal/                # Внутренняя логика
│   │   ├── app/                 # Инициализация приложения
│   │   ├── adapters/            # Адаптеры (БД)
│   │   │   └── storage/postgres/
│   │   ├── cases/               # Бизнес-логика (use cases)
│   │   ├── entities/            # Доменные сущности
│   │   └── ports/               # Внешние интерфейсы
│   │       └── http/            # HTTP обработчики
│   ├── pkg/                     # Публичные пакеты
│   │   └── dto/                 # Data Transfer Objects
│   ├── deployment/              # Настройки развертывания
│   │   ├── config/              # Конфигурация
│   │   └── migrations/          # SQL миграции
│   ├── docker-compose.yml       # Docker оркестрация
│   ├── Dockerfile               # Образ приложения
│   └── go.mod                   # Go зависимости
│
├── docs/                        # Документация
│   └── report.md                # Аналитический отчет
├── mkdocs.yml                   # Конфигурация документации
└── Postman_Collection.json      # Коллекция для тестирования
```

## Архитектура

Проект использует **Clean Architecture** с разделением на слои:

- **Entities** - доменные модели (Newspaper, PrintingHouse, PostOffice, Distribution, User, APIToken)
- **Use Cases** - бизнес-логика (services)
- **Adapters** - реализация репозиториев (PostgreSQL)
- **Ports** - HTTP handlers, middleware

## Технологии

- **Go** 1.23.0
- **Chi Router** - HTTP маршрутизация
- **PostgreSQL** - база данных
- **pgx/v4** - драйвер PostgreSQL
- **JWT** (golang-jwt/jwt/v5) - аутентификация
- **Viper** - конфигурация
- **Docker & Docker Compose** - контейнеризация

## Основные возможности

### Управление данными
- CRUD операции для газет (Newspapers)
- CRUD операции для типографий (Printing Houses)
- CRUD операции для почтовых отделений (Post Offices)
- Управление тиражами (Printing Runs)
- Управление распределением (Distributions)

### Аутентификация и авторизация
- Регистрация пользователей с хешированием паролей (bcrypt)
- JWT-токены со сроком действия 7 дней
- Middleware для проверки аутентификации
- API токены для программного доступа

[Подробное описание Printing House API](printing_house.md)

## API Endpoints

Все endpoints доступны через `/api/v1/`:

### Authentication
- `POST /api/v1/auth/register` - регистрация
- `POST /api/v1/auth/login` - вход
- `GET /api/v1/auth/me` - информация о текущем пользователе

### Newspapers
- `GET /api/v1/newspapers` - список газет
- `GET /api/v1/newspapers/{id}` - получить газету
- `POST /api/v1/newspapers` - создать газету
- `PUT /api/v1/newspapers/{id}` - обновить газету
- `DELETE /api/v1/newspapers/{id}` - удалить газету

### Printing Houses
- `GET /api/v1/printing-houses` - список типографий
- `GET /api/v1/printing-houses/{id}` - получить типографию
- `POST /api/v1/printing-houses` - создать типографию
- `PUT /api/v1/printing-houses/{id}` - обновить типографию
- `DELETE /api/v1/printing-houses/{id}` - удалить типографию

### Post Offices
- `GET /api/v1/post-offices` - список отделений
- `GET /api/v1/post-offices/{id}` - получить отделение
- `POST /api/v1/post-offices` - создать отделение
- `PUT /api/v1/post-offices/{id}` - обновить отделение
- `DELETE /api/v1/post-offices/{id}` - удалить отделение

### Distributions
- `GET /api/v1/distributions` - список распределений
- `GET /api/v1/distributions/{id}` - получить распределение
- `POST /api/v1/distributions` - создать распределение
- `PUT /api/v1/distributions/{id}` - обновить распределение
- `DELETE /api/v1/distributions/{id}` - удалить распределение

## Запуск

### С Docker Compose (рекомендуется)

```bash
cd printing_house_go
docker-compose up -d
```

Приложение будет доступно на `http://localhost:8080`

### Локально

```bash
# 1. Установить зависимости
go mod download

# 2. Запустить PostgreSQL
docker-compose up -d postgres

# 3. Настроить конфигурацию
cp .env.example .env
# Отредактировать .env при необходимости

# 4. Запустить приложение
go run cmd/main.go
```

## Тестирование

Используйте Postman Collection (`Postman_Collection.json`) для тестирования API.

### Тестовые пользователи

После первого запуска доступны:

- **Username:** admin, **Email:** admin@printinghouse.local, **Password:** password123
- **Username:** testuser, **Email:** test@printinghouse.local, **Password:** password123

## Конфигурация

Настройки находятся в `deployment/config/config.yml` и могут быть переопределены переменными окружения:

```yaml
server:
  port: 8080
  host: 0.0.0.0

database:
  host: localhost
  port: 5432
  user: postgres
  password: postgres
  dbname: printing_house
  
jwt:
  secret: your-secret-key
  expiration_days: 7
```

## Миграции

Миграции применяются автоматически при запуске через Docker Compose.

Файлы миграций:
- `001_init_schema.up.sql` - начальная схема
- `002_seed_test_data.sql` - тестовые данные
- `003_add_api_tokens.up.sql` - API токены
- `004_add_users.up.sql` - таблица пользователей

Статус: Завершено
