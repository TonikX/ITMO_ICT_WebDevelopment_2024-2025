from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from .forms import  CustomUserCreationForm, CarForm
from .models import User, Car, Ownership

# Существующее представление для одного владельца
def user_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'project_first_app/user.html', {'user': user})

# Новое представление для списка владельцев
def users_list(request):
    users = User.objects.all()
    return render(request, 'project_first_app/users_list.html', {'users': users})

class CarListView(ListView):
    model = Car
    template_name = 'project_first_app/car_list.html'

class CarDetailView(DetailView):
    model = Car
    template_name = 'project_first_app/car_detail.html'

class CarUpdateView(UpdateView):
    model = Car
    fields = ['registration_number', 'brand', 'model', 'color']
    template_name = 'project_first_app/car_update.html'
    success_url = '/cars/'  # После обновления перенаправляем на список автомобилей

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'project_first_app/register.html', {'form': form})

def home(request):
    return render(request, 'project_first_app/home.html')

def profile(request):
    return render(request, 'project_first_app/profile.html')

def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save()
            # Создаем запись о владении автомобилем для текущего пользователя
            Ownership.objects.create(user=request.user, car=car, start_date="2024-01-01")
            return redirect('user_cars')  # Перенаправляем на страницу с автомобилями пользователя
    else:
        form = CarForm()
    return render(request, 'project_first_app/add_car.html', {'form': form})

def user_cars(request):
    # Получаем все автомобили, которыми владеет текущий пользователь
    cars = Car.objects.filter(ownership__user=request.user)
    return render(request, 'project_first_app/user_cars.html', {'cars': cars})