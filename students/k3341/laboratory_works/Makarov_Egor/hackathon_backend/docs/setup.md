# Установка и запуск

## 1) Установка зависимостей
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 2) Настройка окружения
Скопируйте `.env.example` в `.env`:
```bash
cp .env.example .env
```

## 3) PostgreSQL
Создайте БД и пользователя:
```sql
CREATE DATABASE hackathon_db;
CREATE USER hackathon_user WITH PASSWORD 'hackathon_password';
GRANT ALL PRIVILEGES ON DATABASE hackathon_db TO hackathon_user;
```

## 4) Миграции
```bash
python manage.py makemigrations
python manage.py migrate
```

## 5) Суперпользователь и запуск
```bash
python manage.py createsuperuser
python manage.py runserver
```

## 6) Проверка
- Админка: `/admin/`
- Регистрация: `POST /auth/users/`
- Логин: `POST /auth/token/login/`
- API: `/api/`
