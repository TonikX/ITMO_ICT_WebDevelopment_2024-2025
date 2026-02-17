# Lr4 - Full Stack приложение (Go + Vue.js)

## Описание

Четвёртая лабораторная работа - это полнофункциональное Full Stack приложение с разделением на фронтенд (Vue.js 3 + TypeScript) и бэкэнд (Go REST API).

## Цели работы

- Разработать полнофункциональное веб-приложение
- Интегрировать Go REST API с Vue.js фронтенд-ом
- Работать с современным стеком технологий
- Понять архитектуру Full Stack приложения
- Организовать взаимодействие фронтенда и бэкэнда через REST API

## Архитектура

```
Frontend (Vue.js 3)          Backend (Go)
   Vuetify 3              Printing House API
   TypeScript             Chi Router + PostgreSQL
   Port 5173 (Vite)       Port 8080
                          JWT Authentication
```

## Структура проекта

```
Lr4/
├── printing_house_go/         # Go Backend
│   ├── cmd/                   # Точки входа
│   ├── internal/              # Внутренняя логика
│   │   ├── app/               # Инициализация
│   │   ├── adapters/          # БД адаптеры
│   │   ├── cases/             # Бизнес-логика
│   │   ├── entities/          # Доменные модели
│   │   └── ports/             # HTTP обработчики
│   ├── pkg/                   # Публичные пакеты
│   ├── deployment/            # Конфигурация и миграции
│   ├── docker-compose.yml     # Docker оркестрация
│   └── go.mod                 # Go зависимости
│
├── frontend_go/               # Vue.js 3 Frontend
│   ├── src/
│   │   ├── components/        # Vue компоненты
│   │   ├── views/             # Страницы
│   │   ├── services/          # API сервисы
│   │   ├── stores/            # Pinia stores
│   │   ├── router/            # Vue Router
│   │   └── types/             # TypeScript типы
│   ├── package.json
│   └── vite.config.ts
│
├── docs/                      # Документация
├── mkdocs.yml                 # Конфигурация документации
└── Postman_Collection.json    # API тесты
```

## Технологии Backend

- **Go** 1.23.0
- **Chi Router** - HTTP маршрутизация
- **PostgreSQL** - база данных
- **pgx/v4** - драйвер PostgreSQL
- **JWT** - аутентификация
- **Docker & Docker Compose** - контейнеризация
- **Viper** - управление конфигурацией

## Технологии Frontend

- **Vue.js 3** (Composition API)
- **TypeScript** - типизация
- **Vite** - сборщик
- **Vuetify 3** - UI библиотека
- **Pinia** - state management
- **axios** - HTTP клиент
- **Vue Router** - маршрутизация

## Структура фронтенда

```
frontend_go/src/
├── App.vue              # Главный компонент
├── main.ts              # Точка входа
├── views/               # Страницы
│   ├── HomeView.vue
│   ├── LoginView.vue
│   ├── RegisterView.vue
│   ├── ProfileView.vue
│   ├── NewspapersView.vue
│   ├── PrintingHousesView.vue
│   ├── PostOfficesView.vue
│   ├── PrintingRunsView.vue
│   └── DistributionsView.vue
├── services/
│   └── api.ts           # API клиент (настроен для Go backend)
├── stores/
│   └── auth.ts          # JWT аутентификация
├── router/
│   └── index.ts         # Маршруты с защитой
└── types/
    └── index.ts         # TypeScript интерфейсы
```

## Основные возможности

### Backend (Go API)

- JWT аутентификация с токенами на 7 дней
- CRUD операции для газет, типографий, отделений
- Управление распределением печатных изданий
- Чистая архитектура с разделением слоев
- PostgreSQL с миграциями
- Docker контейнеризация

[Подробное описание Backend API](printing_house.md)

### Frontend (Vue.js)

- Аутентификация пользователей
- Управление профилем
- CRUD интерфейсы для всех сущностей
- Адаптивный дизайн (Vuetify)
- Защищенные маршруты
- Централизованное управление состоянием (Pinia)

[Подробное описание Frontend](printing_house_frontend.md)

## Запуск приложения

### Запуск Backend (Go)

```bash
cd printing_house_go
docker-compose up -d
```

Backend будет доступен на `http://localhost:8080`

### Запуск Frontend (Vue.js)

```bash
cd frontend_go
npm install
npm run dev
```

Frontend будет доступен на `http://localhost:5173`

### Быстрый запуск всего стека

**Linux/Mac:**
```bash
cd frontend_go
./start-fullstack.sh
```

**Windows:**
```cmd
cd frontend_go
start-fullstack.bat
```

## Конфигурация

### Backend конфигурация

`printing_house_go/deployment/config/config.yml`:

```yaml
server:
  port: 8080
  host: 0.0.0.0

database:
  host: postgres
  port: 5432
  user: postgres
  password: postgres
  dbname: printing_house

jwt:
  secret: your-secret-key-change-in-production
  expiration_days: 7
```

### CORS настройка

Backend автоматически разрешает запросы с `http://localhost:5173` (настроено в коде).

## API Endpoints

**Base URL:** `http://localhost:8080/api/v1`

### Authentication
- `POST /api/v1/auth/register` - Регистрация
- `POST /api/v1/auth/login` - Вход
- `GET /api/v1/auth/me` - Текущий пользователь

### Newspapers
- `GET /api/v1/newspapers` - Список газет
- `POST /api/v1/newspapers` - Создать газету
- `GET /api/v1/newspapers/{id}` - Получить газету
- `PUT /api/v1/newspapers/{id}` - Обновить газету
- `DELETE /api/v1/newspapers/{id}` - Удалить газету

### Printing Houses
- `GET /api/v1/printing-houses` - Список типографий
- `POST /api/v1/printing-houses` - Создать типографию
- `GET /api/v1/printing-houses/{id}` - Получить типографию
- `PUT /api/v1/printing-houses/{id}` - Обновить типографию
- `DELETE /api/v1/printing-houses/{id}` - Удалить типографию

### Post Offices
- `GET /api/v1/post-offices` - Список отделений
- `POST /api/v1/post-offices` - Создать отделение
- `GET /api/v1/post-offices/{id}` - Получить отделение
- `PUT /api/v1/post-offices/{id}` - Обновить отделение
- `DELETE /api/v1/post-offices/{id}` - Удалить отделение

### Distributions
- `GET /api/v1/distributions` - Список распределений
- `POST /api/v1/distributions` - Создать распределение
- `GET /api/v1/distributions/{id}` - Получить распределение
- `PUT /api/v1/distributions/{id}` - Обновить распределение
- `DELETE /api/v1/distributions/{id}` - Удалить распределение

## Тестовые пользователи

После запуска backend автоматически создаются:

| Username | Email | Password |
|----------|-------|----------|
| admin | admin@printinghouse.local | password123 |
| testuser | test@printinghouse.local | password123 |

## Тестирование

Используйте Postman Collection (`Postman_Collection.json`) для тестирования API.

Или используйте веб-интерфейс на `http://localhost:5173`.

## Особенности реализации

### Отличия от Python версии

| Аспект | Python (Lr3) | Go (Lr4) |
|--------|--------------|----------|
| Порт | 8000/8001 | 8080 |
| API Base | `/api/` | `/api/v1/` |
| Auth Header | `Token <token>` | `Bearer <token>` |
| Auth Type | Django Token | JWT Token |
| БД | SQLite | PostgreSQL |
| Архитектура | MTV | Clean Architecture |

### Ключевые технические решения

- **Clean Architecture** - разделение на слои для тестируемости
- **Dependency Injection** - инверсия зависимостей
- **Repository Pattern** - абстракция работы с БД
- **JWT** - stateless аутентификация
- **Docker Compose** - одноконтейнерное развертывание
- **Миграции** - версионирование схемы БД

Статус: Завершено
