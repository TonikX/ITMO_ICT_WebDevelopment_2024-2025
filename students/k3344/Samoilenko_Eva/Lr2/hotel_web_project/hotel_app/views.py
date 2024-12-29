from datetime import timedelta, datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DeleteView, UpdateView
from .forms import BookingCreateForm, ReviewWriteForm, CustomUserCreationForm
from .models import *
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('/login/')
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/hotels/')
        else:
            return redirect('/login/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def rooms_list(request, hotel_id):
    rooms = Room.objects.filter(hotel_id=hotel_id)
    return render(request, "hotel/hotel_rooms.html", {"rooms": rooms})


def room_reviews(request, hotel_id, room_id):
    room = Room.objects.get(id=room_id)
    try:
        bookings = Booking.objects.filter(room=room)
        reviews = Review.objects.filter(booking__in=bookings)
    except Booking.DoesNotExist:
        reviews = []
    return render(request, "hotel/room_reviews.html", {"room": room, "reviews": reviews})


@login_required(login_url='/login/')
def book_room(request, hotel_id, room_id):
    room = Room.objects.get(id=room_id)
    user = request.user
    context = {}
    form = BookingCreateForm(request.POST or None)
    if form.is_valid():
        booking = form.save(commit=False)
        booking.user = user
        booking.room = room
        form.save()
        return redirect("bookings")
    context['form'] = form
    return render(request, "booking/book_room.html", context)


@login_required(login_url='/login/')
def write_review(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    context = {}
    form = ReviewWriteForm(
        request.POST or None)
    if form.is_valid():
        review = form.save(commit=False)
        review.booking = booking
        form.save()
        return redirect('room_reviews', booking.room.hotel.id, booking.room.id)
    context['form'] = form
    return render(request, "review/write_review.html", context)


def user_bookings(request):
    bookings = Booking.objects.filter(user_id=request.user)
    return render(request, "booking/user_bookings.html", {"bookings": bookings})


def monthly_clients(request, hotel_id):
    last_month = datetime.now() - timedelta(days=30)
    bookings = Booking.objects.filter(start_date__gt=last_month).filter(room__hotel_id=hotel_id)
    return render(request, "hotel/monthly_clients.html", {"bookings_month": bookings})


class HotelListView(ListView):
    model = Hotel
    context_object_name = 'hotels'
    template_name = 'hotel/hotels_list.html'


class BookingDeleteView(DeleteView):
    model = Booking
    success_url = "/bookings/"
    template_name = 'booking/booking_delete.html'


class BookingUpdateView(UpdateView):
    model = Booking
    fields = ['start_date', 'end_date']
    success_url = '/bookings/'
    template_name = 'booking/booking_update.html'
