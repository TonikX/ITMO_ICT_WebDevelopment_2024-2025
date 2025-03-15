# Практическая работа №2.2

## Задание

Цель работы: дать подробное представление о реализации CRUD(Create, read, update and delete) интерфейсов средствами Django **WEB** фреймворка.<br>
Необходимо выполнить все задлания с пометкой **практическая работа** из [практической работы №2](https://docs.google.com/document/d/1koLV9iGXJfL2yh88InKo4AVXxWqMIJOqmzT4XFYlWuU/edit?usp=sharing).<br>
Полученную программу залить в папку этого репозитория **sutdents/группа/practical_works/фамилия_имя/simple_django_web_project**. Инструкция о загрузке работы ниже. Не забывайте о файле gitignore.

## Code

forms.py:
```python
from django import forms
from .models import Owner

class OwnerForm(forms.ModelForm):
  class Meta:
    model = Owner
    fields = '__all__'
```

views.py:
```python
from django.shortcuts import render
from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .models import Owner, Car
from .forms import OwnerForm

def owner(request, pk):
  try:
    x = Owner.objects.get(pk=pk)
  except Owner.DoesNotExist:
    raise Http404("Owner does not exist")
  return render(request, 'owner.html', {'owner': x})

def owners(request):
  try:
    x = Owner.objects.all()
  except Owner.DoesNotExist:
    raise Http404("Owner does not exist")
  return render(request, 'owners.html', {'owners': x})

class CarList(ListView):
  model = Car
  template_name = 'cars.html'

class CarDetail(DetailView):
  model = Car
  template_name = 'car.html'

def owner_create(request):
  form = OwnerForm(request.POST or None)
  if form.is_valid():
    form.save()
  return render(request, "owner_create.html", {'form': form})

class CarUpdate(UpdateView):
  model = Car
  fields = '__all__'
  template_name = 'car_update.html'
  success_url = '/car/'

class CarCreate(CreateView):
  model = Car
  fields = '__all__'
  template_name = 'car_create.html'
  success_url = '/car/'

class CarDelete(DeleteView):
  model = Car
  template_name = 'car_delete.html'
  success_url = '/car/'
```

urls.py:
```python
from django.urls import path 
from . import views

urlpatterns = [
  path('owner/', views.owners),
  path('owner/<int:pk>/', views.owner),
  path('car/', views.CarList.as_view()),
  path('car/<int:pk>/', views.CarDetail.as_view()),
  path('owner/create/', views.owner_create),
  path('car/<int:pk>/update/', views.CarUpdate.as_view()),
  path('car/create/', views.CarCreate.as_view()),
  path('car/<int:pk>/delete/', views.CarDelete.as_view()),
]
```

.py:
```python
```

.py:
```python
```

car_create.html:
```html
...
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit">
</form>
...
```

car_delete.html:
```html
...
<form method="post">{% csrf_token %}
  <p>Are you sure you want to delete car "{{ object }}"?</p>
  <input type="submit">
</form>
<br><br>
<a href="/car/">Get back</a>
...
```

car_update.html:
```html
...
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit">
</form>
...
```

car.html:
```html
...
Number: {{ object.number }} <br>
Brand: {{ object.brand }} <br>
Model: {{ object.model }} <br>
Color: {{ object.color }}
...
```

cars.html:
```html
...
{% for car in object_list %}
Number: {{ car.number }} <br>
Brand: {{ car.brand }} <br>
Model: {{ car.model }} <br>
Color: {{ car.color }}
{% if not forloop.last %}<hr>{% endif %}
{% endfor %}
...
```

owner_create.html:
```html
...
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit">
</form>
...
```

owner.html:
```html
...
First name: {{ owner.first_name }} <br>
Last name: {{ owner.last_name }} <br>
Date of birth: {{ owner.date_of_birth }}
...
```

owners.html:
```html
...
{% for owner in owners %}
First name: {{ owner.first_name }} <br>
Last name: {{ owner.last_name }} <br>
Date of birth: {{ owner.date_of_birth }}
{% if not forloop.last %}<hr>{% endif %}
{% endfor %}
...
```