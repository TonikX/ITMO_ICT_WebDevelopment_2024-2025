# 📝 Frontend Go - Changelog

## Что изменено для работы с Go Backend

### 🔧 API Service (`src/services/api.ts`)

#### 1. Base URL
```typescript
// Было (Python)
const API_BASE_URL = 'http://localhost:8000'

// Стало (Go)
const API_BASE_URL = 'http://localhost:8080/api/v1'
```

#### 2. Authorization Header
```typescript
// Было (Python)
config.headers.Authorization = `Token ${token}`

// Стало (Go)
config.headers.Authorization = `Bearer ${token}`
```

#### 3. Auth Endpoints

**Login:**
```typescript
// Было (Python)
await this.api.post('/api/auth/login/', { username, password })
// Возвращает: { auth_token }

// Стало (Go)
await this.api.post('/auth/login', { username_or_email, password })
// Возвращает: { token, token_type, expires_at, user }
```

**Register:**
```typescript
// Было (Python)
await this.api.post('/api/auth/register/', { username, password, password_retype })

// Стало (Go)
await this.api.post('/auth/register', { username, email, password, first_name, last_name })
```

#### 4. Endpoints Format

**Python** (с trailing slash):
- `/api/newspapers/`
- `/api/newspapers/1/`
- `/api/newspapers/1/full_detail/`

**Go** (без trailing slash):
- `/newspapers`
- `/newspapers/1`
- `/newspapers/1/full-detail`

#### 5. HTTP Methods

**Python**: PATCH для обновлений
```typescript
this.api.patch(`/api/newspapers/${id}/`, data)
```

**Go**: PUT для обновлений
```typescript
this.api.put(`/newspapers/${id}`, data)
```

#### 6. Response Format

**Python** (с пагинацией):
```json
{
  "count": 10,
  "next": "...",
  "previous": null,
  "results": [...]
}
```

**Go** (массив напрямую):
```json
[
  { "id": 1, ... },
  { "id": 2, ... }
]
```

Адаптация в коде:
```typescript
// Было
async getNewspapers() {
  const response = await this.api.get('/api/newspapers/')
  return response.data // { count, results }
}

// Стало
async getNewspapers() {
  const response = await this.api.get('/newspapers')
  return { results: response.data, count: response.data.length }
}
```

### 🔐 Auth Store (`src/stores/auth.ts`)

#### JWT Token Storage
```typescript
// Go API возвращает больше данных
const response = await api.login(username, password)
// { token, token_type: "Bearer", expires_at, user }

token.value = response.token
user.value = response.user
localStorage.setItem('auth_token', response.token)
localStorage.setItem('user', JSON.stringify(response.user))
```

#### User Object
```typescript
// Python
{ id, username, email }

// Go
{ id, username, email, first_name, last_name, full_name, is_active, created_at }
```

### 📊 Data Mapping

#### Distributions (Распределения)

**Python API:**
```typescript
{
  post_office: 1,    // ID напрямую
  newspaper: 2,
  printing_house: 3,
  quantity: 100
}
```

**Go API:**
```typescript
{
  post_office_id: 1,  // С суффиксом _id
  newspaper_id: 2,
  printing_house_id: 3,
  quantity: 100
}
```

Маппинг в коде:
```typescript
async createDistribution(data) {
  const response = await this.api.post('/distributions', {
    post_office_id: data.post_office,
    newspaper_id: data.newspaper,
    printing_house_id: data.printing_house,
    quantity: data.quantity
  })
}
```

### ❌ Недоступные endpoints

Эти endpoints есть в Python, но нет в Go API:

1. `/api/post-offices/low_quantity/` - газеты с малым количеством
2. `/api/distributions/by_newspaper_and_address/` - распределения по газете и адресу
3. `/auth/users/me/` → заменён на `/auth/me`
4. `/auth/users/set_password/` - смена пароля

Для них возвращаем заглушки:
```typescript
async getPostOfficesLowQuantity() {
  return []
}
```

## 🆕 Новые возможности

### JWT Authentication
- Токены валидны 7 дней
- Автоматическое обновление не требуется
- Токен содержит user_id, username, email

### User Registration
Теперь требует email:
```typescript
register(username, email, password, firstName, lastName)
```

## 📝 Итого изменений

| Файл | Изменения |
|------|-----------|
| `src/services/api.ts` | 200+ строк адаптации под Go API |
| `src/stores/auth.ts` | Полностью переписан под JWT |
| `README.md` | Новая документация |
| `QUICKSTART.md` | Инструкция по запуску |
| `start-fullstack.bat/sh` | Скрипты автозапуска |

## ✅ Тестирование

1. Backend запускается на порту 8080
2. Frontend подключается к `http://localhost:8080/api/v1`
3. JWT токены работают правильно
4. CRUD операции работают
5. Специальные запросы (by-name, by-price) работают

---

**Status:** ✅ Ready for Production  
**Tested:** Go Backend v1.1.0  
**Date:** 2026-02-16
