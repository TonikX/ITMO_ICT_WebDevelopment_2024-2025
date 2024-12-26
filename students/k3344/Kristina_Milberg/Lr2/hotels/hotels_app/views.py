from django.http import Http404
from .models import Guest
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from .forms import GuestForm, RoomForm
from django.urls import reverse_lazy
from .models import Room
from .forms import UserForm

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Перенаправление на страницу входа после регистрации
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})

# Создание номера
class RoomCreateView(CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'room_form.html'
    success_url = reverse_lazy('room_list')

# Обновление номера
class RoomUpdateView(UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'room_form.html'
    success_url = reverse_lazy('room_list')

# Удаление номера
class RoomDeleteView(DeleteView):
    model = Room
    template_name = 'room_confirm_delete.html'
    success_url = reverse_lazy('room_list')


def create_guest(request):
    form = GuestForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('guest_list')  # Перенаправляем на список гостей после создания
    return render(request, 'create_guest.html', {'form': form})

# Представление для списка всех номеров
class RoomListView(ListView):
    model = Room
    template_name = 'room_list.html'
    context_object_name = 'rooms'

# Представление для отображения информации о номере по ID
class RoomDetailView(DetailView):
    model = Room
    template_name = 'room_detail.html'
    context_object_name = 'room'

# Представление для обновления информации о номере
class RoomUpdateView(UpdateView):
    model = Room
    template_name = 'room_update.html'
    fields = ['room_type', 'capacity', 'amenities', 'price']  # Указываем поля, которые можно обновлять
    success_url = reverse_lazy('room_list')  # Перенаправление после успешного обновления

def guest_detail(request, username):
    try:
        user = User.objects.get(username=username)  # Найти пользователя по имени
        guest = Guest.objects.get(user=user)  # Найти гостя, связанного с этим пользователем
    except User.DoesNotExist:
        raise Http404("User does not exist")  # Ошибка, если пользователь не найден
    except Guest.DoesNotExist:
        raise Http404("Guest does not exist")  # Ошибка, если у пользователя нет профиля гостя

    return render(request, 'guest.html', {'guest': guest})

def guest_list(request):
    guests = Guest.objects.all()  # Получаем всех гостей из базы данных
    return render(request, 'guest_list.html', {'guests': guests})

