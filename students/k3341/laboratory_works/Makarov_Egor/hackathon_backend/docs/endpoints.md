# Эндпоинты

> Все эндпоинты (кроме регистрации/логина) требуют заголовок:
> `Authorization: Token <token>`

## Auth (Djoser)
- `POST /auth/users/` — регистрация
- `POST /auth/token/login/` — получить токен
- `POST /auth/token/logout/` — удалить токен
- `GET /auth/users/me/` — текущий пользователь

## Профиль
- `GET /api/profiles/me/`
- `PATCH /api/profiles/me/`

## Теги
- `GET /api/tags/`
- `POST /api/tags/` (ADMIN)

## Задачи
- `GET /api/tasks/` — **вложенные tags/resource_links/resource_files**
- `GET /api/tasks/{id}/`
- `POST /api/tasks/` (ADMIN)

## Ресурсы задач
- `GET/POST /api/task-resource-links/` (POST: CURATOR своей задачи или ADMIN)
- `GET/POST /api/task-resource-files/` (POST: CURATOR своей задачи или ADMIN)

## Команды
- `GET /api/teams/` — **вложенные members**
- `POST /api/teams/` (CAPTAIN)
- `PATCH /api/teams/{id}/` (CAPTAIN своей команды)

## Решения
- `GET /api/solutions/`
- `POST /api/solutions/` (CAPTAIN)
- `PATCH /api/solutions/{id}/` (CAPTAIN своей команды)

## Оценки
- `GET /api/evaluations/`
- `POST /api/evaluations/` (JURY)

## Аналитика (агрегационные запросы)
- `GET /api/analytics/teams_per_task/`
- `GET /api/analytics/avg_score_per_solution/`
- `GET /api/analytics/jury_activity/`
- `GET /api/analytics/curator_load/`
