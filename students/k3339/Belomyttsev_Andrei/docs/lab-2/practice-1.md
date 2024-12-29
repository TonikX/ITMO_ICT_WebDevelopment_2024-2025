# Практическая работа №2.1

## Задание

Цель работы: дать краткое представление о работе Django **WEB** фреймворка.<br>

Необходимо выполнить все задания с пометкой **практическая работа** из [практической работы №1](https://docs.google.com/document/d/1HAJibz51G8bY8tLZB7LFWUZxtnSznRUxwUhE4PsSqys/edit#heading=h.4gydwgvz41hv).<br>
Полученную программу загрузить в папку этого репозитория **sutdents/группа/practical_works/фамилия_имя/simple_django_web_project**. Инструкция о загрузке работы ниже. Не забывайте о файле gitignore.

## Code

admin.py:
```python
from django.contrib import admin
from .models import Owner, License, Car, Ownership

admin.site.register(Owner)
admin.site.register(License)
admin.site.register(Car)
admin.site.register(Ownership)
```

models.py:
```python
from django.db import models

class Owner(models.Model):
  last_name = models.CharField(max_length=30, null=False, blank=False)
  first_name = models.CharField(max_length=30, null=False, blank=False)
  date_of_birth = models.DateField(null=True, blank=True)

  def __str__(self):
    return f'{self.first_name} {self.last_name}'

class License(models.Model):
  owner = models.ForeignKey(Owner, models.CASCADE, null=False, blank=False)
  number = models.CharField(max_length=10, null=False, blank=False)
  type = models.CharField(max_length=10, null=False, blank=False)
  date_of_issue = models.DateField(null=False, blank=False)

  def __str__(self):
    return f'{self.owner}'

class Car(models.Model):
  number = models.CharField(max_length=15, null=False, blank=False)
  brand = models.CharField(max_length=20, null=False, blank=False)
  model = models.CharField(max_length=20, null=False, blank=False)
  color = models.CharField(max_length=30, null=True, blank=True)

  def __str__(self):
    return f'{self.number}, {self.brand}, {self.model}'

class Ownership(models.Model):
  owner = models.ForeignKey(Owner, models.CASCADE, null=True, blank=True)
  car = models.ForeignKey(Car, models.CASCADE, null=True, blank=True)
  start_date = models.DateField(null=False, blank=False)
  end_date = models.DateField(null=True, blank=True)

  def __str__(self):
    return f'{self.car.number}, {self.owner}, {self.start_date} - {self.end_date}'
```

urls.py:
```python
from django.urls import path 
from . import views

urlpatterns = [
  path('owner/<int:owner_id>/', views.owner),
]
```

views.py:
```python
from django.shortcuts import render
from django.http import Http404
from .models import Owner

def owner(request, owner_id):
  try:
    x = Owner.objects.get(pk=owner_id)
  except Owner.DoesNotExist:
    raise Http404("Owner does not exist")
  return render(request, 'owner.html', {'owner': x})
```

owner.html:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Owner</title>
</head>
<body>
  First name: {{ owner.first_name }} <br>
  Last name: {{ owner.last_name }} <br>
  Date of birth: {{ owner.date_of_birth }}
</body>
</html>
```