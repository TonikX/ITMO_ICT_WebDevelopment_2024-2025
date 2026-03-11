# Лабораторная работа — Клиентский интерфейс (Vue.js)

## Цель работы

Реализовать клиентские интерфейсы для системы проведения хакатонов и настроить взаимодействие с серверной частью (Django REST Framework + Djoser).

---

## Стек технологий

| Технология | Версия | Назначение |
|---|---|---|
| Vue.js | 3.x | Реактивный UI-фреймворк |
| Vue Router | 5.x | Клиентская маршрутизация (SPA) |
| Pinia | 3.x | Глобальное состояние (стор) |
| Vite | 7.x | Сборщик / dev-сервер |
| Djoser | 2.x | Токенная авторизация на бэке |
| django-cors-headers | 4.x | CORS для связи фронта с бэком |

---

## Структура проекта (фронтенд)

```
frontend/src/
├── api.js                     # Централизованный fetch-хелпер
├── main.js                    # Точка входа, монтирование приложения
├── App.vue                    # Корневой компонент + глобальные стили
├── router/
│   └── index.js               # Маршруты и навигационные гарды
├── stores/
│   └── auth.js                # Pinia-стор: токен, пользователь, профиль
└── views/
    ├── LoginView.vue          # Страница входа /login
    ├── RegisterView.vue       # Страница регистрации /register
    ├── ProfileView.vue        # Личный профиль /profile
    ├── TasksView.vue          # Список задач /tasks
    ├── DashboardView.vue      # Главный кабинет /dashboard (роут по роли)
    ├── CaptainDashboard.vue   # Кабинет капитана
    ├── CuratorDashboard.vue   # Кабинет куратора
    ├── JuryDashboard.vue      # Кабинет жюри
    └── AdminDashboard.vue     # Кабинет администратора
```

---

## Авторизация и хранение токена

Авторизация реализована через **Djoser Token Authentication**. После успешного логина токен сохраняется в `localStorage` и автоматически подставляется в заголовок `Authorization: Token <token>` при каждом запросе.

**Файл:** `frontend/src/stores/auth.js`

```js
// Логин — получение токена
const res = await fetch('/auth/token/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username, password }),
})
const data = await res.json()
setToken(data.auth_token)  // сохраняем в localStorage
```

После логина сразу загружаются данные пользователя и профиль (роль):

```js
await Promise.all([
  fetch('/auth/users/me/', { headers: authHeaders() }),
  fetch('/api/profiles/me/', { headers: authHeaders() }),
])
```

При регистрации используется поле `re_password` (требуется настройкой Djoser `USER_CREATE_PASSWORD_RETYPE: True`):

```js
body: JSON.stringify({ username, email, password, re_password: password })
```

---

## Маршрутизация и навигационные гарды

**Файл:** `frontend/src/router/index.js`

Реализованы два типа защиты маршрутов:

- `requiresAuth: true` — перенаправляет неавторизованного пользователя на `/login`
- `guestOnly: true` — перенаправляет авторизованного пользователя на `/dashboard`

```js
router.beforeEach(async (to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) return { name: 'login' }
  if (to.meta.guestOnly && auth.isAuthenticated)     return { name: 'dashboard' }
})
```

| Маршрут | Компонент | Доступ |
|---|---|---|
| `/login` | LoginView | Только гости |
| `/register` | RegisterView | Только гости |
| `/dashboard` | DashboardView | Авторизованные |
| `/tasks` | TasksView | Авторизованные |
| `/profile` | ProfileView | Авторизованные |

---

## Ролевые кабинеты

Страница `/dashboard` определяет роль текущего пользователя и динамически подключает нужный компонент:

**Файл:** `frontend/src/views/DashboardView.vue`

```js
const dashComponent = computed(() => {
  if (role.value === 'ADMIN')   return AdminDashboard
  if (role.value === 'JURY')    return JuryDashboard
  if (role.value === 'CURATOR') return CuratorDashboard
  if (role.value === 'CAPTAIN') return CaptainDashboard
  return null
})
```

### Кабинет капитана (`CaptainDashboard.vue`)

Доступные действия:

- Создать команду с названием и девизом
- Выбрать задачу из списка
- Добавить / удалить участников команды (имя, email, роль в команде)
- Просмотреть выбранную задачу: описание, ссылки, файлы, ссылку на консультацию
- Создать решение (черновик или сразу отправить)
- Редактировать черновик решения (отправленное редактировать нельзя)

### Кабинет куратора (`CuratorDashboard.vue`)

Доступные действия:

- Просмотр своей задачи и ссылки на консультацию
- Добавление / удаление ресурсных ссылок к задаче (`POST /api/task-resource-links/`)
- Просмотр решений команд по своей задаче

### Кабинет жюри (`JuryDashboard.vue`)

Доступные действия:

- Просмотр всех поданных решений (с командой и задачей)
- Выставление оценки 0–10 с комментарием (`POST /api/evaluations/`)
- Редактирование своей оценки (`PATCH /api/evaluations/{id}/`)
- Просмотр всех оценок по каждому решению

### Кабинет администратора (`AdminDashboard.vue`)

Доступные действия:

- Создать задачу (название, описание, ссылка на консультацию)
- Редактировать / удалить задачу
- Назначить куратора на задачу прямо из таблицы
- Просмотр всех команд (только чтение)
- Просмотр всех решений со средним баллом (только чтение)

Администратор **не может** создавать команды и оценивать решения — это ограничение отражено в UI (соответствующих кнопок нет).

---

## Настройка CORS

Для работы фронтенда (порт 5173) с бэкендом (порт 8000) был добавлен пакет `django-cors-headers`.

**Файл:** `hackathon_backend/settings.py`

```python
INSTALLED_APPS = [
    "corsheaders",
    ...
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # первым в списке
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```

---

## Интерфейс редактирования профиля

**Файл:** `frontend/src/views/ProfileView.vue`

Пользователь может отредактировать:

- Полное имя (`full_name`)
- Организацию (`organization`)

Поле `role` намеренно не редактируется — это ограничение бэкенда (`UserProfileUpdateSerializer` не включает поле `role`).

Запрос: `PATCH /api/profiles/me/`

---

## Запуск фронтенда

```bash
cd frontend
npm install
npm run dev
```

Приложение будет доступно по адресу `http://localhost:5173`.

Для тестирования разных ролей — создать пользователей через Django shell:

```python
python manage.py shell
```

```python
from django.contrib.auth.models import User
from accounts.models import UserRole

for username, role in [
    ('admin1',   'ADMIN'),
    ('jury1',    'JURY'),
    ('curator1', 'CURATOR'),
    ('captain1', 'CAPTAIN'),
]:
    u, _ = User.objects.get_or_create(username=username)
    u.set_password('Password12345')
    u.save()
    u.profile.role = role
    u.profile.save()
    print(f'{username} готов')
```