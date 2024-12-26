from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import ReservationForm, ReviewForm
from .models import Hotel, Room, Reservation, Review


# Просмотр списка отелей
class HotelListView(ListView):
    model = Hotel
    template_name = 'hotels/hotel_list.html'
    context_object_name = 'hotels'


# Просмотр номеров отеля
def get_room_list(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = hotel.room_set.all()
    today = timezone.now().date()
    user = request.user if request.user.is_authenticated else None

    for room in rooms:
        room.can_leave_review = False
        if user:
            has_review = Review.objects.filter(
                reservation__user=user,
                reservation__room=room
            ).exists()

            if not has_review:
                reservations = Reservation.objects.filter(
                    user=user,
                    room=room,
                    start_date__lte=today
                )
                if reservations.exists():
                    reservations_without_review = reservations.exclude(review__isnull=False)
                    if reservations_without_review.exists():
                        room.can_leave_review = True
                        room.reservation_id_for_review = reservations_without_review.first().id

    context = {'hotel': hotel, 'rooms': rooms}

    if request.user.is_staff:
        one_month_ago = today - timedelta(days=30)
        last_month_guests = Reservation.objects.filter(
            room__hotel=hotel,
            start_date__lte=today,
            end_date__gte=one_month_ago,
        ).order_by('-start_date')
        context['last_month_guests'] = last_month_guests

    return render(request, 'rooms/room_list.html', context)


# Создание бронирования
@login_required(login_url='/login/')
def create_reservation(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.room = room
            reservation.save()
            return redirect('reservation_list')
    else:
        form = ReservationForm()
    return render(request, 'reservations/create_reservation.html', {'form': form, 'room': room})


# Просмотр бронирований пользователя
class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'reservations/reservation_list.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date()
        return context


# Редактирование бронирования
class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservations/update_reservation.html'
    success_url = reverse_lazy('reservation_list')

    def dispatch(self, request, *args, **kwargs):
        reservation = self.get_object()
        if reservation.start_date < timezone.now().date():
            messages.error(request, "Вы не можете редактировать бронь, если дата начала уже прошла.")
            return redirect('reservation_list')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


# Удаление бронирования
class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation
    template_name = 'reservations/delete_reservation.html'
    success_url = reverse_lazy('reservation_list')

    def dispatch(self, request, *args, **kwargs):
        reservation = self.get_object()
        if reservation.start_date < timezone.now().date():
            messages.error(request, "Вы не можете удалить бронь, если дата начала уже прошла.")
            return redirect('reservation_list')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


# Оставление отзыва
@login_required(login_url='/login/')
def create_review(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if hasattr(reservation, 'review'):
        messages.error(request, "Вы уже оставили отзыв для этого бронирования.")
        return redirect('room_reviews', room_id=reservation.room.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.reservation = reservation
            review.save()
            return redirect('room_reviews', room_id=reservation.room.id)
    else:
        form = ReviewForm()
    return render(request, 'rooms/create_review.html', {'form': form, 'reservation': reservation})


# Просмотр отзывов для номера
def get_room_reviews(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    reviews = Review.objects.filter(reservation__room=room)
    return render(request, 'rooms/room_reviews.html', {'room': room, 'reviews': reviews})


# Регистрация пользователя
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')


# Вход пользователя
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('hotel_list')
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


# Выход пользователя
@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    messages.info(request, "Вы успешно вышли из аккаунта.")
    return redirect('login')
