# Подробное описание Racing App

## Архитектура приложения

Racing App представляет собой полнофункциональное Django приложение для управления автогонками с использованием встроенной админ-панели.

## Модели данных

### User
Расширенная модель AbstractUser с дополнительными полями:

```python
class User(AbstractUser):
    EXPERIENCE_LEVEL = [
        ('NB', 'Новичок'),
        ('SP', 'Любитель'),
        ('PR', 'Профессионал'),
    ]
    
    experience = CharField()          # Уровень опыта
    driver_class = CharField()        # Класс гонщика
    bio = TextField()                 # Биография
```

### Team
Модель команды:

```python
class Team(models.Model):
    name = CharField(unique=True)     # Уникальное название
    description = TextField()         # Описание команды
```

### Car
Реестр автомобилей:

```python
class Car(models.Model):
    owner = OneToOneField(User)       # Владелец машины
    team = ForeignKey(Team)           # Команда, к которой относится авто
    model = CharField()               # Модель автомобиля
    description = TextField()         # Описание авто
    year = PositiveIntegerField()     # Год выпуска
```

### Race
Модель гонки:

```python
class Race(models.Model):
    name = CharField()                # Название гонки
    description = TextField()         # Описание
    date = DateTimeField()            # Дата и время заезда
    location = CharField()            # Место проведения
    is_active = BooleanField()        # Активна ли гонка
```

## Функциональность

### Управление пользователями
- Регистрация гонщиков
- Классификация по уровню опыта
- Присвоение класса гонщика

### Управление командами
- Создание команд
- Привязка автомобилей к командам

### Управление автомобилями
- Регистрация автомобилей для гонщиков
- Связь владелец-автомобиль (OneToOne)
- Привязка к команде

### Управление гонками
- Создание новых гонок
- Планирование даты и места
- Управление активностью гонки

## Admin Panel

Django встроенная админ-панель позволяет:
- Создавать и редактировать гонщиков
- Управлять командами
- Регистрировать автомобили
- Создавать гонки
- Фильтровать и искать данные

## Установка и запуск

### Зависимости

```bash
pip install -r requirements.txt
```

### Инициализация БД

```bash
python manage.py migrate
```

### Запуск dev сервера

```bash
python manage.py runserver
```

Приложение будет доступно: http://localhost:8000/

### Вход в админ-панель

```
http://localhost:8000/admin/
```

Создайте суперпользователя для входа:
```bash
python manage.py createsuperuser
```

## Технологии

- Django 4.x+
- Python 3.x
- SQLite (по умолчанию)
- PostgreSQL (опционально)

Дополнительно: [Вернуться к обзору Lr2](index.md)
