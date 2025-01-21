# ЛАБОРАТОРНАЯ РАБОТА №2

# РЕАЛИЗАЦИЯ ПРОСТОГО САЙТА СРЕДСТВАМИ DJANGO

## Цель:

Овладеть практическими навыками и умениями реализации web-сервисов
средствами Django 2.2.

## Описание

Реализовать сайт используя фреймворк Django 3 и СУБД PostgreSQL *, в
соответствии с вариантом задания лабораторной работы.

## Стек

Python 3.6+, Django 3, PostgreSQL *.

## Список научных конференций
Интерфейс описывает названия конференций, список тематик, место проведения,
период проведения, описание конференций, описание место проведения, условия участия.
Необходимо реализовать следующий функционал:

- Регистрация новых пользователей.
- Просмотр конференций и регистрацию авторов для выступлений.
Пользователь должен иметь возможность редактирования и удаления своих
регистраций.
- Написание отзывов к конференциям. При добавлении комментариев,
должны сохраняться даты конференции, текст комментария, рейтинг (1-10),
информация о комментаторе.
- Администратор должен иметь возможность указания результатов
выступления (рекомендован к публикации или нет) средствами Django-
admin.
- В клиентской части должна формироваться таблица, отображающая всех
участников по конференциям.

## Настройка

- настройка Postgres
```bash
sudo -u postgres psql
CREATE ROLE confadmin WITH LOGIN SUPERUSER PASSWORD '12345678';
CREATE DATABASE conferences;
CTRL+Z
sudo systemctl restart postgresql.service
```

- подключение Postgres
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "conferences",
        "USER": "confadmin",
        "PASSWORD": "12345678",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

## Модели

```python
class Conference(models.Model):
    title = models.TextField()
    description = models.TextField()
    starting_at = models.DateField()
    ending_at = models.DateField()
    themes = models.TextField()
    location = models.TextField()


class Presentation(models.Model):
    name = models.TextField()
    description = models.TextField()
    duration = models.PositiveIntegerField()
    conference = models.ForeignKey(Conference, related_name='presentations', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='author', on_delete=models.DO_NOTHING)


class Registration(models.Model):
    user = models.ForeignKey(User, related_name='registrations', on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, related_name='registrations', on_delete=models.CASCADE)
    is_author = models.BooleanField(default=False)
    presentation = models.ForeignKey(Presentation, related_name='presentations', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Registration {self.user.username} - {self.conference.title}"


class Review(models.Model):
    registration = models.ForeignKey(Registration, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(10),
    ])
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.registration.user.username} - {self.registration.conference.title}"
```

### Эндпоинты

```python
    path('signup/', views.signup, name='signup'),
    path('', views.conferences_list, name='conf_list'),
    path('conferences/<int:conf_id>/presentations/', views.presentations_list, name='presentations_list'),
    path('registrations/<int:conf_id>/make_presentation/', views.make_presentation, name='make_presentation'),
    path('registrations/<int:conf_id>/enroll/', views.enroll, name='enroll'),
    path('registrations/', views.my_registrations, name='my_registrations'),
    path('registrations/<int:registration_id>/edit/', views.edit_registration, name='edit_registration'),
    path('registrations/<int:registration_id>/delete/', views.delete_registration, name='delete_registration'),
    path('registrations/<int:registration_id>/review/', views.add_review, name='add_review'),
    path('participants/', views.participants, name='participants'),
```