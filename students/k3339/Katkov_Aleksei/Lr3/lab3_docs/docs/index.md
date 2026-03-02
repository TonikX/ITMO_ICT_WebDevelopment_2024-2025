# Лабораторная работа №3

Реализация серверной части приложения средствами Django REST Framework

## Используемые технологии

-   Python
-   Django
-   Django REST Framework
-   Djoser (Token Authentication)
-   PostgreSQL

------------------------------------------------------------------------

## Модель данных

### User

Используется встроенная модель пользователя Django.

### Category

-   id
-   title
-   description
-   owner (ForeignKey -\> User)

Связь: один пользователь может иметь несколько категорий.

### Task

-   id
-   title
-   description
-   status (todo / in_progress / done)
-   created_at
-   category (ForeignKey -\> Category)
-   owner (ForeignKey -\> User)

Связи: - один пользователь может иметь несколько задач - одна категория
может содержать несколько задач

------------------------------------------------------------------------

## Авторизация

Реализована через Djoser с использованием токенов.

### Регистрация пользователя

POST /auth/users/

### Получение токена

POST /auth/token/login/

Пример запроса:

``` json
{
  "username": "user",
  "password": "password"
}
```

Ответ:

``` json
{
  "auth_token": "token_value"
}
```

### Использование токена

    Authorization: Token token_value

------------------------------------------------------------------------

## Реализованные эндпоинты

### Категории

-   GET /api/categories/
-   POST /api/categories/
-   GET /api/categories/{id}/
-   PUT/PATCH /api/categories/{id}/
-   DELETE /api/categories/{id}/
-   GET /api/categories/full/

### Задачи

-   GET /api/tasks/
-   POST /api/tasks/
-   GET /api/tasks/{id}/
-   PUT/PATCH /api/tasks/{id}/
-   DELETE /api/tasks/{id}/
-   GET /api/tasks/full/

------------------------------------------------------------------------

## Практическая работа 3.1 (Django ORM)

Практика выполнялась в:

    python manage.py shell

### Проверка количества объектов

``` python
from django.contrib.auth.models import User
from api.models import Category, Task

User.objects.count()
Category.objects.count()
Task.objects.count()
```

### Фильтрация

``` python
Task.objects.filter(status="todo")
Task.objects.filter(title__icontains="лаба")
Category.objects.filter(title__icontains="уч")
```

### Фильтрация по связям

``` python
Category.objects.filter(owner__username="oleg")
Task.objects.filter(category__title="Быт")
Task.objects.filter(owner__username="anna")
```

### Сортировка

``` python
Task.objects.order_by("-created_at")
Task.objects.order_by("title")
```

### Агрегация

``` python
from django.db.models import Min, Max

Task.objects.aggregate(oldest=Min("created_at"))
Task.objects.aggregate(latest=Max("created_at"))
```

### Аннотация

``` python
from django.db.models import Count

User.objects.annotate(task_count=Count("tasks")).values("username", "task_count")
Category.objects.annotate(task_count=Count("tasks")).values("title", "task_count")
```

### Группировка

``` python
Task.objects.values("status").annotate(cnt=Count("id")).order_by("status")
```

### distinct

``` python
Category.objects.filter(tasks__isnull=False).distinct()
```

------------------------------------------------------------------------

## Итог

В рамках лабораторной работы были реализованы:

-   Django ORM (filter, aggregate, annotate, values, order_by, distinct)
-   Django REST Framework (CRUD через generics)
-   Nested сериализация
-   Авторизация через Djoser (TokenAuthentication)
-   Работа с PostgreSQL
-   Документирование API через MkDocs
