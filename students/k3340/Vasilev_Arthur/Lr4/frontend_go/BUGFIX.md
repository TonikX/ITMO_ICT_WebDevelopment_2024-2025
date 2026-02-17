# 🔧 Исправление ошибок входа/регистрации

## Что было исправлено:

### 1. **Добавлено поле Email в форму регистрации**
   - Go API требует обязательное поле `email`
   - Добавлено поле email в `RegisterView.vue`

### 2. **Исправлена функция register в auth store**
   - Было: `register(username, password, passwordRetype)`
   - Стало: `register(username, email, password)`

### 3. **Добавлен CORS middleware в Go backend**
   - Разрешены запросы с `http://localhost:5173`
   - Добавлены необходимые заголовки

### 4. **Обновлены зависимости**
   - Добавлен `github.com/go-chi/cors v1.2.1`
   - Обновлён `go.sum`

## 🚀 Как проверить:

### Шаг 1: Убедитесь, что backend запущен

```bash
cd Lr3/printing_house_go
docker-compose ps
```

Должны быть 2 контейнера в состоянии `Up`.

### Шаг 2: Перезапустите frontend

```bash
# Остановите frontend (Ctrl+C)
# Запустите заново
cd Lr4/frontend_go
npm run dev
```

### Шаг 3: Откройте браузер

```
http://localhost:5173
```

### Шаг 4: Попробуйте войти

**Тестовый пользователь:**
- Username: `admin`
- Password: `password123`

Нажмите "Sign In" - должен войти успешно.

### Шаг 5: Попробуйте зарегистрироваться

1. Нажмите "Create one"
2. Заполните форму:
   - **Username:** myuser
   - **Email:** myuser@example.com (ОБЯЗАТЕЛЬНО!)
   - **Password:** mypassword123
   - **Confirm Password:** mypassword123
3. Нажмите "Create Account"

Должна пройти регистрация и автоматический вход.

## 🐛 Если всё ещё не работает:

### Проверка 1: Backend доступен?

Откройте в браузере:
```
http://localhost:8080/api/v1/newspapers
```

Должен вернуться JSON с массивом газет.

### Проверка 2: Проверьте консоль браузера

1. Откройте DevTools (F12)
2. Вкладка "Console"
3. Попробуйте войти
4. Посмотрите ошибки

**Типичные ошибки:**

**CORS Error:**
```
Access to XMLHttpRequest at 'http://localhost:8080/api/v1/auth/login' 
from origin 'http://localhost:5173' has been blocked by CORS policy
```

**Решение:** Backend уже обновлён с CORS middleware. Перезапустите backend:
```bash
cd Lr3/printing_house_go
docker-compose restart app
```

**Network Error:**
```
Network Error
```

**Решение:** Backend не запущен. Запустите:
```bash
cd Lr3/printing_house_go
docker-compose up -d
```

**401 Unauthorized:**
```
{"error": "invalid credentials"}
```

**Решение:** Неверный пароль. Используйте `password123` для admin/testuser.

### Проверка 3: Логи backend

```bash
cd Lr3/printing_house_go
docker-compose logs -f app
```

Должны видеть запросы от frontend.

## 📝 Тестовые данные

### Существующие пользователи в БД:

| Username | Email | Password |
|----------|-------|----------|
| admin | admin@printinghouse.local | password123 |
| testuser | test@printinghouse.local | password123 |

### Регистрация нового пользователя:

**Обязательные поля:**
- ✅ Username (уникальный)
- ✅ Email (уникальный, валидный)
- ✅ Password

**Опциональные поля:**
- First Name
- Last Name

## 🔑 JWT Token

После успешного входа/регистрации:
- Token сохраняется в `localStorage` под ключом `auth_token`
- User сохраняется в `localStorage` под ключом `user`
- Token валиден **7 дней**
- Token автоматически добавляется ко всем API запросам

## ✅ Checklist

- [ ] Backend запущен (docker-compose ps)
- [ ] Backend отвечает (http://localhost:8080/api/v1/newspapers)
- [ ] Frontend запущен (npm run dev)
- [ ] Браузер открыт на http://localhost:5173
- [ ] CORS middleware включен в backend
- [ ] Email поле добавлено в форму регистрации

Если всё отмечено ✅ - должно работать!

---

**Дата исправления:** 2026-02-16  
**Файлы изменены:**
- `Lr4/frontend_go/src/views/RegisterView.vue`
- `Lr3/printing_house_go/internal/ports/http/server.go`
- `Lr3/printing_house_go/go.mod`
- `Lr3/printing_house_go/go.sum`
