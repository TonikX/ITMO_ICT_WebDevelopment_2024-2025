# Alpine Clubs (Лабораторная работа №3)

## Описание
**Alpine Clubs** — это REST API для управления альпинистскими клубами, маршрутами и восхождениями. Он предоставляет возможность регистрации альпинистских клубов, управления участниками и отслеживания восхождений.

## Features
- Авторизация и аутентификация юзеров (djoser).
- Управление альпинистскими клубами (создание, участие, выход из клуба).
- Список гор и маршрутов для восхождений.
- Управление восхождениями и участниками.
- Фильтрация по стране, городу, маршруту и др.

## Getting Started
### Системные требования
- Python 3.10+
- Django 4+
- Django REST Framework
- PostgreSQL / SQLite

### Установка
1. Клонируй репозиторий:
   ```sh
   git clone https://github.com/penkovgd/ITMO_ICT_WebDevelopment_2024-2025
   cd alpine-clubs-manager
   ```
2. Создай и активируй виртуальное окружение:
   ```sh
   python -m venv venv
   source venv/bin/activate  # Для Linux/macOS
   venv\Scripts\activate  # Для Windows
   ```
3. Выполни миграции:
   ```sh
   python manage.py migrate
   ```
4. Создай суперпользователя:
   ```sh
   python manage.py createsuperuser
   ```
5. Запусти сервер:
   ```sh
   python manage.py runserver
   ```

### Документация API
Swagger-UI: `http://127.0.0.1:8000/api/schema/swagger/`

ReDoc: `http://127.0.0.1:8000/api/schema/redoc/`