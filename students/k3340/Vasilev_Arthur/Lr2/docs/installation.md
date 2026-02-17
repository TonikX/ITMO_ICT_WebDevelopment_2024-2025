# Установка и настройка

## Системные требования

- Python 3.8+
- PostgreSQL 12+
- Git

## Установка зависимостей

1. **Клонируйте репозиторий:**
   ```bash
   git clone <repository-url>
   cd racing_project
   ```

2. **Создайте виртуальное окружение:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или
   venv\Scripts\activate     # Windows
   ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

## Настройка базы данных

1. **Создайте базу данных PostgreSQL:**
   ```sql
   CREATE DATABASE racing_db;
   CREATE USER racing_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE racing_db TO racing_user;
   ```

2. **Настройте подключение в settings.py:**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'racing_db',
           'USER': 'racing_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

## Миграции и запуск

1. **Выполните миграции:**
   ```bash
   python manage.py migrate
   ```

2. **Создайте суперпользователя:**
   ```bash
   python manage.py createsuperuser
   ```

3. **Запустите сервер разработки:**
   ```bash
   python manage.py runserver
   ```

4. **Откройте браузер:**
   Перейдите на http://127.0.0.1:8000

## Доступ к админке

- URL: http://127.0.0.1:8000/admin/
- Используйте учетные данные суперпользователя

## Структура URL

- `/` - Главная страница
- `/races/` - Список гонок
- `/register/` - Регистрация пользователя
- `/login/` - Вход в систему
- `/admin/` - Админка Django