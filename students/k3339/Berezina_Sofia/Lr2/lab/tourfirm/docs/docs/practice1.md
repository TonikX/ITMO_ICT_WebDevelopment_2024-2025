## Практическое задание 1: Необходимо установить Django Web framework любым доступным способом

Формат именований файлов:

- Формат имени Django-проекта: “django*project*фамилия”.

- Формат имени Django-приложения: “project_first_app”.

### Выполнение задания

1. В папке `practice` я создала папку для проекта `django_project_berezina`
2. В ней я создала виртуальное окружение `tutorial-env` и, установив нужные библиотеки, создала django-приложение `project_first_app`:

```bash
python -m venv tutorial-env
source tutorial-env/bin/activate

pip install django

django-admin startproject django_project_berezina
cd django_project_berezina

python manage.py startapp project_first_app
```

3. В `settings.py` добавляем наше приложение:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'project_first_app',
]
```

## Практическое задание 2.1: В проекте создать модель данных об автовладельцах в соответствии с рисунком 2

![Рисунок 2](<Снимок экрана 2025-10-22 в 13.46.34.png>)

### Выполнение задания

```python
from django.db import models

class Car(models.Model):
    car_id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30)

class CarOwner(models.Model):
    owner_id = models.AutoField(primary_key=True)
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    birth_date = models.DateField()


class CarLicense(models.Model):
    license_id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey(CarOwner, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    issue_date = models.DateField()

class Ownership(models.Model):
    car_owner_id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey(CarOwner, on_delete=models.CASCADE)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
```

## Практическое задание 2.2: Создать миграции и применить их к базе данных

```python
python manage.py makemigrations
python manage.py migrate
```

## Практическое задание 3

Необходимо заполнить таблицы данными средствами админ-панели. Зарегистрировать владельца авто в админ-панели.

- Необходимо зайти в файл `admin.py` в папке приложения (\*\_app) и зарегистрировать владельца автомобиля следующими командами:

```python
from .models import Название владельца в модели данных #то, что указано в кавычках - это какие либо параметры, которые Вам нужно ввести самостоятельно, в соответствии с Вашим проектом. В Конкретном случае, Вам нужно указать название таблицы модели данных, которую необходимо отразить в админ-панеле.

admin.site.register(Название владельца в модели данных)
```

- Зарегистрировать остальные таблицы модели данных в админ-панели.

- Создать суперпользователя командой:

```python
python manage.py createsuperuser
```

- Запустить сервер командой:

```python
python manage.py runserver
```

- Зайти в админ-панель по url-адресу (127.0.0.1:8000/admin/) и добавить двух владельцев автомобилей, 4 автомобиля. Далее связать каждого владельца минимум с тремя автомобилями, так, чтобы не было пересечений по датам владения и продажи.

### Выполнение задания:

1. Для начала зарегестрируем наши модели:

```python
from django.contrib import admin
from .models import Ownership, Car, CarLicense, CarOwner

admin.site.register(Car)
admin.site.register(CarOwner)
admin.site.register(CarLicense)
admin.site.register(Ownership)
```

2. Создаем суперпользователя, запускаем сервер и добавляем владельцев автомобилей и сами автомобили в админ-панели

```python
python manage.py createsuperuser
python manage.py runserver
```

## Практическое задание 4

Создать в файле `views.py` (находится в папке приложения) представление (контроллер), который выводит из базы данных данные о владельце автомобиля. Создать страницу html-шаблона owner.html в папке templates (создать папку templates в корне проекта, если ее нигде нет, далее в контекстном меню папки создать html-файл). Страница должна содержать отображение полей переданных из контроллера.

### Выполнение задания

1. В `views.py` добавляем функцию для передачи параметров из базы данных:

```python
from django.shortcuts import render, get_object_or_404
from .models import CarOwner

def detail(request, owner_id):
    owner = get_object_or_404(CarOwner, owner_id=owner_id)

    return render(request, "owner.html", {
        'name': owner.name,
        'surname': owner.surname
    })
```

2. Создаем папку templates и файл `owner.html`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Title</title>
  </head>
  <body>
    Имя: {{ name }}, Фамилия: {{ surname }}
  </body>
</html>
```

## Практическое задание 5

Создать файл адресов urls.py в папке приложения (\*\_app) (пока пустой). Импортировать файл urls.py приложения в проект (модифицировать файл urls.py в той папке, в которой хранится файл setting.py).

Теперь необходимо описать в файле urls.py приложения, созданном в пункте 4.1.1, такой url-адрес, который сможет обратиться к контроллеру и вывести страницу, которая должна быть отрендерена контроллером.

Необходимо обратиться к контроллеру, который создан в задаче 4 и передать параметр (иденфикационный номер владельца) в адресной строке

### Выполнение задания

1. В `urls.py` создаем паттерн для подключения к html странице

```python
from django.urls import path
from project_first_app import views

urlpatterns = [
    path('owner/<int:owner_id>/', views.detail, name='owner'),
]
```

![alt text](<Снимок экрана 2025-10-22 в 14.28.32.png>)
