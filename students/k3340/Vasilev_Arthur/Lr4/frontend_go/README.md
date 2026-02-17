# 🎨 Frontend для Go Backend (Printing House)

Vue 3 + TypeScript фронтенд для системы управления типографией на Go.

## 🔗 Связь с Backend

Этот frontend настроен для работы с **Go backend** (`Lr3/printing_house_go`):
- **Backend URL**: `http://localhost:8080`
- **API Base**: `http://localhost:8080/api/v1`
- **Auth Type**: JWT Bearer Token

## 📋 Основные отличия от Python версии

| Аспект | Python Backend | Go Backend |
|--------|----------------|------------|
| Порт | 8000 | 8080 |
| API Base | `/api/` | `/api/v1/` |
| Auth Header | `Token <token>` | `Bearer <token>` |
| Auth Type | Django Token | JWT Token |
| Пагинация | Django Paginator | Без пагинации |
| Endpoints | Trailing slash `/` | Без trailing slash |

## 🚀 Установка и запуск

### 1. Установить зависимости

```bash
cd frontend_go
npm install
```

### 2. Запустить Go Backend

```bash
cd ../Lr3/printing_house_go
docker-compose up -d
```

Подождать ~15 секунд для инициализации БД.

### 3. Запустить Frontend

```bash
cd ../Lr4/frontend_go
npm run dev
```

Frontend будет доступен на `http://localhost:5173`

## 🔐 Аутентификация

### Тестовые пользователи

| Username | Email | Password |
|----------|-------|----------|
| admin | admin@printinghouse.local | password123 |
| testuser | test@printinghouse.local | password123 |

### JWT Token

После логина или регистрации JWT токен сохраняется в `localStorage`:
- Key: `auth_token`
- Format: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
- Срок действия: 7 дней

Токен автоматически добавляется ко всем запросам в заголовке:
```
Authorization: Bearer <jwt_token>
```

## 📚 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Регистрация
- `POST /api/v1/auth/login` - Логин
- `GET /api/v1/auth/me` - Получить текущего пользователя

### Newspapers
- `GET /api/v1/newspapers` - Список газет
- `GET /api/v1/newspapers/{id}` - Получить газету
- `POST /api/v1/newspapers` - Создать газету
- `PUT /api/v1/newspapers/{id}` - Обновить газету
- `DELETE /api/v1/newspapers/{id}` - Удалить газету

### Printing Houses
- `GET /api/v1/printing-houses` - Список типографий
- `GET /api/v1/printing-houses/{id}` - Получить типографию
- `POST /api/v1/printing-houses` - Создать типографию
- `PUT /api/v1/printing-houses/{id}` - Обновить типографию
- `DELETE /api/v1/printing-houses/{id}` - Удалить типографию

### Post Offices
- `GET /api/v1/post-offices` - Список почтовых отделений
- `GET /api/v1/post-offices/{id}` - Получить почтовое отделение
- `POST /api/v1/post-offices` - Создать почтовое отделение
- `PUT /api/v1/post-offices/{id}` - Обновить почтовое отделение
- `DELETE /api/v1/post-offices/{id}` - Удалить почтовое отделение

### Distributions
- `GET /api/v1/distributions` - Список распределений
- `GET /api/v1/distributions/{id}` - Получить распределение
- `POST /api/v1/distributions` - Создать распределение
- `PUT /api/v1/distributions/{id}` - Обновить распределение
- `DELETE /api/v1/distributions/{id}` - Удалить распределение

## 🔧 Конфигурация

### Изменить URL Backend

Отредактируйте `src/services/api.ts`:

```typescript
const API_BASE_URL = 'http://localhost:8080/api/v1'
```

### CORS

Backend должен разрешать запросы с `http://localhost:5173`:

```go
// В Go backend уже настроен CORS для development
```

## 📁 Структура проекта

```
frontend_go/
├── src/
│   ├── components/      # Vue компоненты
│   ├── views/          # Страницы (routes)
│   ├── router/         # Vue Router настройка
│   ├── stores/         # Pinia stores (auth, etc)
│   ├── services/       # API service (адаптирован под Go)
│   └── assets/         # Статические файлы
├── public/             # Публичные файлы
└── package.json        # Зависимости
```

## 🎯 Основные изменения в коде

### API Service (`src/services/api.ts`)

**Было (Python):**
```typescript
const API_BASE_URL = 'http://localhost:8000'
config.headers.Authorization = `Token ${token}`
```

**Стало (Go):**
```typescript
const API_BASE_URL = 'http://localhost:8080/api/v1'
config.headers.Authorization = `Bearer ${token}`
```

### Auth Store (`src/stores/auth.ts`)

**Было (Python):**
```typescript
const response = await api.login(username, password)
token.value = response.auth_token
```

**Стало (Go):**
```typescript
const response = await api.login(username, password)
token.value = response.token
user.value = response.user
```

## 🧪 Тестирование

### 1. Проверить Backend

```bash
curl http://localhost:8080/api/v1/newspapers
```

Должен вернуться список газет (HTTP 200)

### 2. Открыть Frontend

```
http://localhost:5173
```

### 3. Залогиниться

- Username: `admin`
- Password: `password123`

### 4. Протестировать функции

- ✅ Создание газеты
- ✅ Редактирование газеты
- ✅ Удаление газеты
- ✅ Просмотр типографий
- ✅ Создание распределений

## 🐛 Troubleshooting

### Frontend не может подключиться к Backend

**Проблема:** `Network Error` или `ERR_CONNECTION_REFUSED`

**Решение:**
```bash
# Проверить, что Go backend запущен
cd Lr3/printing_house_go
docker-compose ps

# Если не запущен - запустить
docker-compose up -d

# Проверить логи
docker-compose logs app
```

### 401 Unauthorized

**Проблема:** JWT токен истёк или недействителен

**Решение:**
1. Выйдите из системы (logout)
2. Залогиньтесь заново
3. JWT токены валидны 7 дней

### CORS Error

**Проблема:** `Access-Control-Allow-Origin` error

**Решение:**
Go backend должен разрешать requests с `http://localhost:5173`. Проверьте CORS настройки в Go коде.

## 📚 Документация Backend

- **[Lr3/printing_house_go/README.md](../Lr3/printing_house_go/README.md)** - Общая документация Go API
- **[Lr3/printing_house_go/REGISTRATION.md](../Lr3/printing_house_go/REGISTRATION.md)** - JWT аутентификация
- **[Lr3/printing_house_go/TESTING.md](../Lr3/printing_house_go/TESTING.md)** - Тестирование API

## 🔗 Связанные проекты

- **Backend (Go)**: `Lr3/printing_house_go/`
- **Backend (Python)**: `Lr4/printing_house/`
- **Frontend (Python)**: `Lr4/frontend/`
- **Frontend (Go)**: `Lr4/frontend_go/` (этот проект)

---

**Version:** 1.0.0  
**Stack:** Vue 3 + TypeScript + Vite  
**Backend:** Go 1.23 + Chi Router + PostgreSQL  
**Author:** Vasilev Arthur
