# Лабораторная работа 2: Django приложение для автогонок

## Описание проекта

Веб-приложение для управления автогонками, разработанное с использованием Django 4.2 и PostgreSQL. Приложение позволяет управлять участниками автогонок, командами, автомобилями, гонками и комментариями.

## Основной функционал

### Для пользователей:
- **Регистрация и аутентификация**
- **Просмотр доступных гонок**
- **Регистрация на гонки**
- **Управление своими регистрациями** (редактирование, удаление)
- **Написание отзывов и комментариев** к гонкам
- **Просмотр результатов гонок**

### Для администраторов:
- **Управление гонками** (создание, редактирование)
- **Установка времени и результатов заездов**
- **Управление пользователями и командами**
- **Модерация комментариев**

## Архитектура приложения

### Модели данных

#### User (Пользователь)
Расширенная модель пользователя Django с дополнительными полями для гонок.

```python
class User(AbstractUser):
    EXPERIENCE_LEVEL = [
        ('NB', 'Новичок'),
        ('SP', 'Любитель'),
        ('PR', 'Профессионал'),
    ]

    experience = models.CharField(
        'Уровень опыта',
        max_length=2,
        choices=EXPERIENCE_LEVEL,
        default='NB'
    )
    driver_class = models.CharField(
        'Класс гонщика',
        max_length=50,
        blank=True,
        null=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True
    )
```

#### Team (Команда)
Модель для команд участников.

```python
class Team(models.Model):
    name = models.CharField(
        'Название команды',
        max_length=100,
        unique=True
    )
    description = models.TextField(
        'Описание команды',
        blank=True,
        null=True
    )
```

#### Car (Автомобиль)
Модель автомобиля участника.

```python
class Car(models.Model):
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='car',
        verbose_name='Владелец'
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cars',
        verbose_name='Команда'
    )
    model = models.CharField(
        'Модель автомобиля',
        max_length=100
    )
    description = models.TextField(
        'Описание автомобиля'
    )
    year = models.PositiveIntegerField(
        'Год выпуска',
        null=True,
        blank=True
    )
```

#### Race (Гонка)
Модель гонки.

```python
class Race(models.Model):
    name = models.CharField(
        'Название гонки',
        max_length=200
    )
    description = models.TextField(
        'Описание гонки',
        blank=True,
        null=True
    )
    date = models.DateTimeField(
        'Дата и время заезда'
    )
    location = models.CharField(
        'Место проведения',
        max_length=200,
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        'Активная гонка',
        default=True
    )
```

#### RaceRegistration (Регистрация на гонку)
Связь между пользователем и гонкой.

```python
class RaceRegistration(models.Model):
    racer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='registrations',
        verbose_name='Гонщик'
    )
    race = models.ForeignKey(
        Race,
        on_delete=models.CASCADE,
        related_name='registrations',
        verbose_name='Гонка'
    )
    registration_date = models.DateTimeField(
        'Дата регистрации',
        auto_now_add=True
    )
    result = models.CharField(
        'Результат',
        max_length=100,
        blank=True,
        null=True
    )
    final_time = models.DurationField(
        'Финальное время',
        blank=True,
        null=True
    )
    position = models.PositiveIntegerField(
        'Позиция',
        blank=True,
        null=True
    )
```

#### Comment (Комментарий)
Модель комментариев к гонкам.

```python
class Comment(models.Model):
    COMMENT_TYPES = [
        ('COOP', 'Вопрос о сотрудничестве'),
        ('RACE', 'Вопрос о гонках'),
        ('OTHER', 'Иное'),
    ]

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    race = models.ForeignKey(
        Race,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Гонка'
    )
    text = models.TextField('Текст комментария')
    type = models.CharField(
        'Тип комментария',
        max_length=5,
        choices=COMMENT_TYPES,
        default='RACE'
    )
    rating = models.IntegerField(
        'Рейтинг',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    is_approved = models.BooleanField(
        'Одобрен',
        default=True
    )
```

### Представления (Views)

#### Классовые представления

**RaceListView** - Отображает список всех активных гонок.
**RaceDetailView** - Показывает детальную информацию о гонке с комментариями.
**RaceRegistrationView** - Обрабатывает регистрацию пользователя на гонку.

#### Функциональные представления

**user_profile** - Отображает профиль пользователя с его регистрациями.
**add_comment** - Добавляет комментарий к гонке.

### Шаблоны (Templates)

Приложение использует систему шаблонов Django с Bootstrap для стилизации:

- **base.html** - Базовый шаблон с навигацией
- **race_list.html** - Список доступных гонок
- **race_detail.html** - Детальная информация о гонке
- **user_profile.html** - Профиль пользователя
- **Формы регистрации и комментариев**

### Админка Django

Настроена расширенная админка для управления всеми моделями:

- **CustomUserAdmin** - Управление пользователями с дополнительными полями
- **TeamAdmin** - Управление командами
- **CarAdmin** - Управление автомобилями
- **RaceAdmin** - Управление гонками
- **RaceRegistrationAdmin** - Управление регистрациями
- **CommentAdmin** - Модерация комментариев с действиями одобрения/отклонения

## Технологии

- **Backend:** Django 4.2.7
- **База данных:** PostgreSQL
- **Frontend:** HTML, CSS, Bootstrap 5.1.3
- **Аутентификация:** Django Auth
- **Админка:** Django Admin

## Установка и запуск

### Системные требования
- Python 3.8+
- PostgreSQL 12+
- Git

### Установка зависимостей
```bash
git clone <repository-url>
cd racing_project
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Настройка базы данных
```sql
CREATE DATABASE racing_db;
CREATE USER racing_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE racing_db TO racing_user;
```

### Миграции и запуск
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Структура проекта

```
racing_project/
├── racing_app/
│   ├── models.py          # Модели данных
│   ├── views.py           # Представления
│   ├── urls.py            # Маршруты
│   ├── forms.py           # Формы
│   ├── admin.py           # Админка
│   └── templates/         # Шаблоны
├── manage.py
├── requirements.txt       # Зависимости
└── settings.py           # Настройки
```

## Особенности реализации

- **Безопасность:** Использование Django ORM для защиты от SQL-инъекций
- **Масштабируемость:** Классовые представления для повторного использования кода
- **Пользовательский опыт:** Bootstrap для responsive дизайна
- **Администрирование:** Полнофункциональная админка для управления данными
- **Валидация:** Формы с валидацией данных на стороне сервера