from .models import CarOwner, Car
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView
from django.urls import reverse_lazy
from .forms import CarOwnerForm, CarForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CarOwnerForm



def car_owner_detail(request, owner_id):
    try:
        # получаем объект CarOwner по его первичному ключу (id)
        owner = CarOwner.objects.get(pk=owner_id)
    except CarOwner.DoesNotExist:
        raise Http404("Car owner does not exist")

    return render(request, 'owner.html', {'owner': owner})


def owners_list(request):
    owners = CarOwner.objects.all()  # Получаем всех владельцев из базы данных
    return render(request, 'owners_list.html', {'owners': owners})  # Передаем их в шаблон


class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'
    context_object_name = 'cars'

class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
    context_object_name = 'car'

class CarUpdateView(UpdateView):
    model = Car
    template_name = 'car_update.html'
    fields = ['license_plate', 'brand', 'model', 'color']
    success_url = reverse_lazy('car_list')


def add_car_owner(request):
    if request.method == 'POST':
        form = CarOwnerForm(request.POST)
        if form.is_valid():
            form.save()  # Сохранение нового владельца
            return redirect('add_car_owner')  # Перенаправление на страницу после успешного сохранения
    else:
        form = CarOwnerForm()

    owners = CarOwner.objects.all()  # Получение всех владельцев для отображения
    return render(request, 'car_owner_app/add_car_owner.html', {'form': form, 'owners': owners})


def car_list(request):
    cars = Car.objects.all()
    return render(request, 'car_list.html', {'cars': cars})

def add_car(request):
    if request.method == "POST":
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('car_list')
    else:
        form = CarForm()
    return render(request, 'car_form.html', {'form': form})

def update_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == "POST":
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect('car_list')
    else:
        form = CarForm(instance=car)
    return render(request, 'car_form.html', {'form': form})

def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == "POST":
        car.delete()
        return redirect('car_list')
    return render(request, 'car_confirm_delete.html', {'car': car})


def create_car_owner(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        owner_form = CarOwnerForm(request.POST)

        if user_form.is_valid() and owner_form.is_valid():
            user = user_form.save()
            owner = owner_form.save(commit=False)
            owner.user = user
            owner.save()
            return redirect('car_list')  # или другая страница, куда нужно перенаправить
    else:
        user_form = UserCreationForm()
        owner_form = CarOwnerForm()

    return render(request, 'create_car_owner.html', {
        'user_form': user_form,
        'owner_form': owner_form,
    })
