### Условие
Django Web framework. CRUD(Create, read, update and delete) интерфейсы средствами Django WEB фреймворка
1. Реализовать форму ввода всех владельцев функционально.
Добавить данные минимум о еще трех владельцах. Должны быть реализованы форма (Form), контроллер (views) и шаблоны (templates).
2. Реализовать форму ввода, обновления и удаления всех автомобилей на основе классов. Добавить данные минимум о еще трех автомобилях. Должны быть реализованы  форма (Form), контроллер (views) и шаблоны (temlates).


### 
Листинг кода, forms.py:
``` py hl_lines="2 3"

from django import forms
from .models import *

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = [
            "last_name",
            "first_name",
            "birth_date",
            "passport_number",
            "nationality",
            "home_address"
        ]
        widgets = {
            'password': forms.PasswordInput(),
        }


class CreateCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["state_number", "brand", "model", "color"]
        labels = {
            "state_number": "Number",
            "brand": "Brand",
            "model": "Model",
            "color": "Color",
        }


class UpdateCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["state_number", "brand", "model", "color"]
        labels = {
            "state_number": "Number",
            "brand": "Brand",
            "model": "Model",
            "color": "Color",
        }


```

Листинг кода, views.py:
``` py hl_lines="2 3"

from django.shortcuts import render

# Create your views here.
from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.views.generic.edit import DeletionMixin

from .forms import OwnerForm
from .models import Owner, Car


def owner(request, owner_id):
    try:
        owner_model = Owner.objects.get(id=owner_id)
    except Owner.DoesNotExist:
        raise Http404("Owner does not exist")
    return render(request, 'owner.html', {'owner': owner_model})


def owners(request):
    context = {"owners": Owner.objects.all()}

    return render(request, "owners.html", context)


def create_owner(request):
    context = {}
    form = OwnerForm(
        request.POST or None)
    if form.is_valid():
        form.save()
    context['form'] = form
    return render(request, "owner_create.html", context)


class CarsList(ListView):
    model = Car
    context_object_name = 'cars'
    template_name = 'cars.html'


class CarRetrieveView(DetailView):
    model = Car
    template_name = 'car.html'


class CarCreateView(CreateView):
    model = Car
    template_name = 'car_create.html'
    fields = ['state_number', 'brand', 'model', 'color']
    success_url = '/cars/'


class CarUpdateView(UpdateView):
    model = Car
    template_name = 'car_update.html'
    fields = ['state_number', 'brand', 'model', 'color']
    success_url = '/cars/'


class CarDeleteView(DeleteView):
    model = Car
    success_url = '/cars/'
    template_name = 'car_delete.html'


```

В templates реализованы шаблоны:

    car.html
    car_create.html
    car_delete.html
    car_update.html
    cars.html
    owner.html
    owner_create.html
    owners.html