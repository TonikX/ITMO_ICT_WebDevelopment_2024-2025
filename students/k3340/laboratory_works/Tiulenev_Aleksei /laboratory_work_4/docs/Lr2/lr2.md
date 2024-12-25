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

## Доска домашних заданий.

О домашнем задании должна храниться следующая информация: предмет,
преподаватель, дата выдачи, период выполнения, текст задания, информация о штрафах.

Необходимо реализовать следующий функционал:
- Регистрация новых пользователей.
- Просмотр домашних заданий по всем дисциплинам (сроки выполнения,
описание задания).
- Сдача домашних заданий в текстовом виде.
- Администратор (учитель) должен иметь возможность поставить оценку за
задание средствами Django-admin.
- В клиентской части должна формироваться таблица, отображающая оценки
всех учеников класса.

## Настройка

- настройка Postgres
```bash
sudo -u postgres psql
CREATE ROLE homeworks WITH LOGIN SUPERUSER PASSWORD '12345678';
CREATE DATABASE lr2_homeworks;
CTRL+Z
sudo systemctl restart postgresql.service
```

- подключение Postgres
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "lr2_homeworks",
        "USER": "web_lr2",
        "PASSWORD": "12345678",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

## Модели

```python
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from lr2.settings import Statuses
import hashlib
import datetime


class Class(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Student(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=256)
    name = models.CharField(max_length=40)
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    def set_password(self, raw_password):
        hashed_password = hashlib.sha256(raw_password.encode('utf-8')).hexdigest()
        self.password = hashed_password

    def check_password(self, raw_password):
        return hashlib.sha256(raw_password.encode('utf-8')).hexdigest() == self.password


class Task(models.Model):
    title = models.TextField()
    description = models.TextField()
    created_at = models.DateField()
    expire_at = models.DateField()
    author = models.CharField(max_length=100)
    student_classes = models.ManyToManyField(Class)

    def __str__(self):
        return self.title

    @property
    def is_past_due(self):
        return datetime.date.today() > self.expire_at


class Assignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    text = models.TextField()
    grade = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5),
    ], null=True, blank=True)
    graded_at = models.DateField(null=True, blank=True)
    received_at = models.DateField()

    status = models.IntegerField(validators=[
        MinValueValidator(min(Statuses)),
        MaxValueValidator(max(Statuses)),
    ], default=1)

    class Meta:
        unique_together = ('task', 'student')

    def __str__(self):
        return f'{self.student.name}: {self.task.title}'
```

### Эндпоинты

```python
urlpatterns = [
    path('', MainView.as_view(), name='root'),
    path('signup/', SignUpStudentView.as_view(), name='signup'),
    path('signin/', SignInStudentView.as_view(), name='signin'),
    path('logout/', LogoutAccountView.as_view(), name='logout'),
    path('tasks/', TasksView.as_view(), name='tasks_list'),
    path('tasks/<int:pk>', TaskDetailView.as_view(), name='task_details'),
    path('tasks/<int:task_id>/create_assignment', AssignmentCreateView.as_view(), name='create_assignment'),
    path('grades', GradesTableView.as_view(), name='grades_table')
]
```
