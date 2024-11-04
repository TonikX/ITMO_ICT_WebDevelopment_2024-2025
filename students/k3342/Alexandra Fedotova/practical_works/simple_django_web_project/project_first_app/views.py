from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from .models import CarOwner, Car
from .forms import CarForm, CarOwnerForm, CustomUserForm
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
import datetime


def create_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('home')  # Перенаправление на главную страницу или другую после создания пользователя
    else:
        form = CustomUserForm()
    return render(request, 'create_user.html', {'form': form})


def owner_detail(request, owner_id):
    try:
        owner = CarOwner.objects.get(pk=owner_id)
    except CarOwner.DoesNotExist:
        raise Http404("Owner does not exist")

    # Включите информацию о пользователе
    user_info = {
        'passport_number': owner.user.passport_number,
        'home_address': owner.user.home_address,
        'nationality': owner.user.nationality,
    }

    return render(request, 'carowner.html', {'owner': owner, 'user_info': user_info})


def example_view(request):
    now = datetime.datetime.now()
    html = "Time is {}".format(now)
    return HttpResponse(html)


# Классовое представление для списка всех автомобилей
class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'
    context_object_name = 'cars'


# Классовое представление для создания автомобиля
class CarCreateView(CreateView):
    model = Car
    form_class = CarForm
    template_name = 'car_form.html'  # Используйте car_form.html для создания и обновления
    success_url = reverse_lazy('car_list')


# Классовое представление для обновления автомобиля
class CarUpdateView(UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'car_form.html'
    success_url = reverse_lazy('car_list')


# Классовое представление для удаления автомобиля
class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_confirm_delete.html'
    success_url = reverse_lazy('car_list')


# Классовое представление для детализации автомобиля
class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
    context_object_name = 'car'


def add_and_list_car_owners(request):
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST)
        owner_form = CarOwnerForm(request.POST)

        if user_form.is_valid() and owner_form.is_valid():
            user = user_form.save(commit=False)

            # Генерация уникального имени пользователя
            user.username = f"user_{user.passport_number}_{get_random_string(5)}"

            user.save()  # Сохранение пользователя
            car_owner = owner_form.save(commit=False)
            car_owner.user = user  # Привязка владельца к пользователю
            car_owner.save()  # Сохранение владельца

            return redirect('car_owners')  # Перенаправить на страницу списка владельцев
    else:
        user_form = CustomUserForm()
        owner_form = CarOwnerForm()

    # Получить всех владельцев для отображения
    owners = CarOwner.objects.all()
    return render(request, 'car_owners_list.html', {'user_form': user_form, 'owner_form': owner_form, 'owners': owners})