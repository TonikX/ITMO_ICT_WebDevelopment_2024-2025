from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import SignUpForm, ReservationForm, ReviewForm
from .models import Hotel, RoomType, Room, Reservation
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('hotel_list')
    else:
        form = SignUpForm()
    return render(request, 'bookings/signup.html', {'form': form})


def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'bookings/hotel_list.html', {'hotels': hotels})


def room_list(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    room_types = hotel.room_types.all()
    return render(request, 'bookings/room_list.html', {'hotel': hotel, 'room_types': room_types})


@login_required
def make_reservation(request, room_type_id):
    room_type = get_object_or_404(RoomType, id=room_type_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        form.fields['room'].queryset = room_type.rooms.all()
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            return redirect('my_reservations')
    else:
        form = ReservationForm()
        form.fields['room'].queryset = room_type.rooms.all()
    return render(request, 'bookings/make_reservation.html', {'form': form, 'room_type': room_type})


@login_required
def my_reservations(request):
    reservations = request.user.reservations.all()
    return render(request, 'bookings/my_reservations.html', {'reservations': reservations})


@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('my_reservations')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'bookings/edit_reservation.html', {'form': form})


@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        reservation.delete()
        return redirect('my_reservations')
    return render(request, 'bookings/delete_reservation.html', {'reservation': reservation})


@login_required
def add_review(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reservation = reservation
            review.save()
            return redirect('my_reservations')
    else:
        form = ReviewForm()
    return render(request, 'bookings/add_review.html', {'form': form})


def guest_list(request):
    last_month = timezone.now() - timedelta(days=30)
    reservations = Reservation.objects.filter(check_in__gte=last_month, is_checked_in=True)
    return render(request, 'bookings/guest_list.html', {'reservations': reservations})
