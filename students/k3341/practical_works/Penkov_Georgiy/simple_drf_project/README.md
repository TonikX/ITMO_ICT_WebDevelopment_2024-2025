# Практические работы лабораторной работы №3

Этот django проект содержит 2 приложения:
1. cars - практическая работа №3.1
2. warriors - практическая работа №3.2

## Запуск проекта

1: Создайте и активируйте виртуальное окружение

```
python -m venv .venv
```
Для Windows:
```
.venv\Scripts\activate
```
Для macOS/Linux:
```
source .venv/bin/activate
```

2: Примените миграции
```
python manage.py migrate
```

3: Запустите сервер
```
python manage.py runserver
```
4: Откройте проект в браузере
Перейдите по адресу http://127.0.0.1:8000