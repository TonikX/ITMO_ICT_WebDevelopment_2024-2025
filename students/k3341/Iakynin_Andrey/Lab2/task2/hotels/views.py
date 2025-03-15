import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, UpdateView

from hotels.forms import UserRegistrationForm, UserLoginForm, BookingForm, ReviewForm, HotelForm, \
    RoomForm
from hotels.models import Hotel, Room, Booking
from django.contrib import messages
from django.core.paginator import Paginator


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/registration_form.html', {'user_form': user_form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('hotel_list')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid username or password')
    else:
        form = UserLoginForm()
        return render(request, 'account/login.html', {'form': form})


@login_required
def hotel_list(request):
    query = request.GET.get('q')
    hotels = Hotel.objects.all()

    if query:
        hotels = hotels.filter(name__icontains=query)

    paginator = Paginator(hotels, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'hotel/hotels.html', {'page_obj': page_obj, 'query': query})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main')


def hotel_rooms(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = Room.objects.filter(hotel=hotel).order_by('id')
    paginator = Paginator(rooms, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'hotel/rooms.html', {'hotel': hotel,'page_obj': page_obj})


@login_required
def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    hotel = room.hotel
    booking_form = BookingForm()
    review_form = ReviewForm()
    bookings = Booking.objects.filter(user=request.user, room=room)

    return render(request, 'reservation/reservation.html', {
        'room': room,
        'booking_form': booking_form,
        'review_form': review_form,
        'hotel': hotel,
        'bookings': bookings
    })


@login_required
def booking_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    hotel = room.hotel

    if request.method == "POST":
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.save()
            messages.success(request,
                             f'Резервирование номера успешно создано для пользователя {request.user.username}!')
            return redirect('rooms_detail', room_id=room_id)
    else:
        booking_form = BookingForm()

    return render(request, 'reservation/reservation.html', {
        'room': room,
        'hotel': hotel,
        'booking_form': booking_form,
    })


@login_required
def room_reviews(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    reviews = room.reviews.all()

    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.room = room
            review.save()
            return redirect('room_reviews', room_id=room_id)
    else:
        review_form = ReviewForm()

    return render(request, 'reservation/review_room.html', {
        'room': room,
        'review_form': review_form,
        'reviews': reviews
    })


class BookingDeleteView(DeleteView):
    model = Booking
    template_name = "reservation/reservations_delete.html"
    success_url = reverse_lazy('rooms_detail')

    def get_success_url(self):
        room_id = self.object.room.id
        return reverse_lazy('rooms_detail', kwargs={'room_id': room_id})


class BookingUpdateView(UpdateView):
    model = Booking
    fields = ["check_in", "check_out"]
    template_name = "reservation/reservations_update.html"
    success_url = reverse_lazy('rooms_detail')

    def get_success_url(self):
        room_id = self.object.room.id
        return reverse_lazy('rooms_detail', kwargs={'room_id': room_id})


def last_month_guests(request):
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    bookings = Booking.objects.filter(check_in__gte=last_month)
    return render(request, 'hotel/last_month_guests.html', {'month_bookings': bookings})


@login_required
def check_out_user(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.user.is_superuser:
        booking.delete()
        messages.success(request, 'Бронирование успешно удалено.')
    else:
        messages.error(request, 'У вас нет прав для удаления бронирования.')

    return redirect('bookings')


@login_required
def add_hotel(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = HotelForm(request.POST)
            if form.is_valid():
                hotel = form.save(commit=False)
                hotel.owner = request.user
                hotel.save()
                messages.success(request, 'Новый отель успешно добавлен!')
                return redirect('hotel_list')
        else:
            form = HotelForm()
        return render(request, 'hotel/add_hotel.html', {'form': form})
    else:
        messages.error(request, 'У вас нет прав для добавления отелей.')
        return redirect('hotel_list')


@login_required
def delete_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    if request.user.is_superuser:
        hotel.delete()
        messages.success(request, 'Отель успешно удален.')
    else:
        messages.error(request, 'У вас нет прав для удаления отелей.')
    return redirect('hotel_list')


@login_required
def add_room(request, hotel_id):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = RoomForm(request.POST)
            if form.is_valid():
                room = form.save(commit=False)
                room.hotel_id = hotel_id
                room.save()
                messages.success(request, 'Комната успешно добавлена.')
                return redirect('hotel_rooms', hotel_id=hotel_id)
        else:
            form = RoomForm()

        return render(request, 'hotel/add_room.html', {'form': form, 'hotel_id': hotel_id})
    else:
        messages.error(request, 'У вас нет прав для добавления комнат')
        return redirect('rooms')


@login_required
def delete_room(request, hotel_id, room_id):
    room = get_object_or_404(Room, id=room_id, hotel_id=hotel_id)
    if request.user.is_superuser:
        room.delete()
        messages.success(request, 'Комната успешно удалена.')
        return redirect('hotel_rooms', hotel_id=hotel_id)
    else:
        messages.error(request, 'У вас нет прав для удаления этой комнаты.')
        return redirect('hotel_rooms', hotel_id=hotel_id)


def main(request):
    return render(request, 'main.html')

