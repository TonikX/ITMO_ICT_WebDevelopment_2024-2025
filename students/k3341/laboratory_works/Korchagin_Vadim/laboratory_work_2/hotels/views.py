from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import login, logout
from .models import Room, Booking, Review
from .forms import UserRegistrationForm, BookingForm, ReviewForm
from datetime import timedelta
from django.utils import timezone


# Регистрация нового пользователя
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('room_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


# Просмотр списка доступных номеров
def room_list(request):
    search_query = request.GET.get('search', '')  # Получаем поисковый запрос, если он есть

    if search_query: # Если запрос есть, фильтруем номера по отелю или типу комнаты
        rooms = Room.objects.filter(
            hotel__name__icontains=search_query
        ) | Room.objects.filter(
            room_type__name__icontains=search_query
        )
    else: # Если нет запроса, выбираем все номера
        rooms = Room.objects.all()

    paginator = Paginator(rooms, 2)  # Количество объектов на страницу
    page_number = request.GET.get('page') # Получаем номер страницы из GET-запроса
    page_obj = paginator.get_page(page_number) # Получаем текущую страницу с объектами

    return render(request, 'room_list.html', {'page_obj': page_obj, 'search_query': search_query})

# Подробная информация о конкретном номере
def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    reviews = Review.objects.filter(booking__room=room) # Отзывы, связанные с этим номером
    return render(request, 'room_detail.html', {'room': room, 'reviews': reviews})

# Создание бронирования для конкретного номера
@login_required
def booking_create(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, room=room)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.status = 'pending'
            booking.save()
            messages.success(request, 'Бронирование создано успешно!')
            return redirect('booking_list')
    else:
        form = BookingForm()
    return render(request, 'booking_form.html', {'form': form, 'room': room})

# Список бронирований текущего пользователя
@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking_list.html', {'bookings': bookings})

# Обновление информации о бронировании
@login_required
def booking_update(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    # Проверка, что пользователь является владельцем бронирования
    if booking.user != request.user:
        messages.error(request, 'Вы не можете редактировать это бронирование.')
        return redirect('booking_list')

    # Проверка, что бронь уже кончилась
    if booking.status == 'completed':
        messages.error(request, 'Вы уже не можете обновить это бронирование.')
        return redirect('booking_list')

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Бронирование обновлено успешно!')
            return redirect('booking_list')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'booking_form.html', {'form': form, 'booking': booking})

# Удаление бронирования
@login_required
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if booking.user != request.user:
        messages.error(request, 'Вы не можете удалить это бронирование.')
        return redirect('booking_list')

    if booking.status == 'completed':
        messages.error(request, 'Вы уже не можете удалить это бронирование.')
        return redirect('booking_list')

    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Бронирование удалено успешно!')
        return redirect('booking_list')
    return render(request, 'booking_confirm_delete.html', {'booking': booking})

# Добавление отзыва к бронированию
def add_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Проверка, существует ли уже отзыв для этого бронирования
    if Review.objects.filter(booking=booking).exists():
        messages.error(request, 'Вы уже создали отзыв.')
        return redirect('booking_list')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking # Привязываем отзыв к бронированию
            review.save()
            messages.success(request, 'Отзыв оставлен успешно!')
            return redirect('booking_list')
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'booking': booking})

# Просмотр последних гостей за месяц (доступен только суперпользователю)
@user_passes_test(lambda user: user.is_superuser)
def recent_guests(request):
    last_month = timezone.now().date() - timedelta(days=30) # Вычисление даты месяц назад
    guests = Booking.objects.filter(
        status='completed',
        end_date__gte=last_month
    ).select_related('user', 'room', 'room__hotel') # Выборка завершенных бронирований за последний месяц
    return render(request, 'recent_guests.html', {'guests': guests})

# Главная страница
def home(request):
    return render(request, 'home.html')
