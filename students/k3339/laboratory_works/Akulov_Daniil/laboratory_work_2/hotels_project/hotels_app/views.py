from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate, logout, login as login_request
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Avg
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DeleteView, UpdateView
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from .forms import HotelCreateForm, RoomCreateForm, BookingCreateForm, BookingAdminCreateForm, ReviewCreateForm
from .models import Room, Booking, Hotel, Review

def custom_404_view(request, exception):
    return render(request, 'error.html', {"message": 'Извините, но запрашиваемая страница не найдена.'})

def registration(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/login/")
    else:
        form = UserCreationForm()
    return render(request, "registration.html", {"form": form})

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login_request(request, user)
            return redirect("/rooms/")
        else:
            return redirect("/login/")
    return render(request, "login.html")

@login_required(login_url='/login/')
def hotels(request):
    hotels = request.user.hotels.all().order_by('id')
    return render(request, "hotels.html", {"hotels": hotels})

@login_required(login_url='/login/')
def hotel_create(request):
    user = request.user
    context = {}
    form = HotelCreateForm(request.POST or None)
    if form.is_valid():
        hotel = form.save(commit=False)
        hotel.owner = user
        form.save()
        return redirect("/hotels/")
    context['form'] = form
    return render(request, "hotel_create.html", context)

class HotelUpdateView(LoginRequiredMixin, UpdateView):
    model = Hotel
    fields = ['name', 'description', 'address']
    success_url = '/hotels/'
    template_name = 'hotel_update.html'
    pk_url_kwarg = "hotel_id"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return render(self.request, 'error.html', {"message": f'Извините, но у вас нет доступа для редактирования Отеля "{self.object.name}".'})

class HotelDeleteView(LoginRequiredMixin, DeleteView):
    model = Hotel
    success_url = '/hotels/'
    template_name = 'hotel_delete.html'
    pk_url_kwarg = "hotel_id"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return render(self.request, 'error.html', {"message": f'Извините, но у вас нет доступа для удаления Отеля "{self.object.name}".'})

def rooms(request):
    rooms = Room.objects.annotate(average_rating=Avg('reviews__rating')).order_by('id')
    return render(request, "rooms.html", {"rooms": rooms})

@login_required(login_url='/login/')
def hotel_rooms(request, hotel_id):
    try:
        hotel = Hotel.objects.get(id=hotel_id)
    except Hotel.DoesNotExist:
        raise Http404("Poll does not exist")
    user = request.user
    if(hotel.owner != user):
        return render(request, 'error.html',
                      {"message": f'Извините, но у вас нет доступа для просмотра комнат Отеля "{hotel.name}".'})
    rooms = hotel.rooms.all().order_by('number')
    return render(request, "hotel_rooms.html", {"rooms": rooms, 'hotel': hotel})

@login_required(login_url='/login/')
def room_create(request, hotel_id):
    try:
        hotel = Hotel.objects.get(id=hotel_id)
    except Hotel.DoesNotExist:
        raise Http404("Poll does not exist")
    user = request.user
    if(hotel.owner != user):
        return render(request, 'error.html',
                      {"message": f'Извините, но у вас нет доступа для просмотра комнат Отеля "{hotel.name}".'})
    context = {}
    form = RoomCreateForm(request.POST or None)
    if form.is_valid():
        room = form.save(commit=False)
        room.hotel = hotel
        form.save()
        return redirect(f'/{hotel_id}/rooms')
    context['form'] = form
    return render(request, "room_create.html", context)

class RoomUpdateView(LoginRequiredMixin, UpdateView):
    model = Room
    fields = ['number', 'price', 'room_type', 'capacity', 'description']
    template_name = 'room_update.html'
    pk_url_kwarg = "room_id"
    success_url = '/rooms/'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.hotel.owner != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return render(self.request, 'error.html', {"message": f'Извините, но у вас нет доступа для редактирования комнаты Отеля "{self.object.hotel.name}".'})

class RoomDeleteView(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = 'room_delete.html'
    pk_url_kwarg = "room_id"
    success_url = '/rooms/'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.hotel.owner != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return render(self.request, 'error.html', {"message": f'Извините, но у вас нет доступа для удаления комнаты Отеля "{self.object.hotel.name}".'})

@login_required(login_url='/login/')
def bookings(request):
    user = request.user
    bookings = user.bookings.all().order_by('-check_in')
    return render(request, "bookings.html", {"bookings": bookings})

@login_required(login_url='/login/')
def hotel_bookings(request, hotel_id):
    try:
        hotel = Hotel.objects.get(id=hotel_id)
    except Hotel.DoesNotExist:
        raise Http404("Poll does not exist")
    users = request.user
    if(hotel.owner != users):
        return render(request, 'error.html',
                      {"message": f'Извините, но у вас нет доступа для просмотра бронирований комнат Отеля "{hotel.name}".'})
    bookings = []
    rooms = hotel.rooms.all()
    for room in rooms:
        for booking in room.bookings.all():
            bookings.append(booking)
    bookings.sort(key=lambda booking: booking.check_in, reverse=True)
    return render(request, "hotel_bookings.html", {"bookings": bookings, 'hotel': hotel})

@login_required(login_url='/login/')
def booking_create(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        raise Http404("Poll does not exist")
    user = request.user
    context = {}
    form = BookingCreateForm(request.POST or None)
    if form.is_valid():
        booking = form.save(commit=False)
        overlapping_bookings = room.bookings.filter(
            check_in__lt=booking.check_in,
            check_out__gt=booking.check_out
        )
        if overlapping_bookings.exists():
            return render(request, 'error.html',
                      {"message": f'Извините, в эти дни номер уже забронирован.'})
        booking.room = room
        booking.user = user
        form.save()
        return redirect(f'/rooms/')
    context['form'] = form
    context['room'] = room
    return render(request, "booking_create.html", context)

@login_required(login_url='/login/')
def booking_admin_create(request, hotel_id):
    try:
        hotel = Hotel.objects.get(id=hotel_id)
    except Hotel.DoesNotExist:
        raise Http404("Poll does not exist")
    user = request.user
    if(hotel.owner != user):
        return render(request, 'error.html',
                      {"message": f'Извините, но у вас нет доступа к Отелю "{hotel.name}".'})
    context = {}
    form = BookingAdminCreateForm(request.POST or None)
    if form.is_valid():
        booking = form.getData()
        booking_username = booking['username']
        try:
            booking_user = User.objects.get(username=booking_username)
        except User.DoesNotExist:
            return render(request, 'error.html',
                      {"message": f'Извините, но пользователь с username "{booking_username}" не найден.'})
        booking_room_number = booking['room_number']
        try:
            booking_room = Room.objects.get(number=booking_room_number)
        except Room.DoesNotExist:
            return render(request, 'error.html',
                      {"message": f'Извините, но комната с номером "{booking_room_number}" не найдена.'})
        overlapping_bookings = booking_room.bookings.filter(
            check_in__lt=booking['check_in'],
            check_out__gt=booking['check_out']
        )
        if overlapping_bookings.exists():
            return render(request, 'error.html',
                      {"message": f'Извините, в эти дни номер уже забронирован.'})
        Booking.objects.create(user=booking_user, room=booking_room, check_in=booking['check_in'], check_out=booking['check_out'])
        return redirect(f'/{hotel_id}/rooms/')
    context['form'] = form
    context['hotel'] = hotel
    return render(request, "booking_admin_create.html", context)

class BookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    fields = ['check_in', 'check_out']
    template_name = 'booking_update.html'
    pk_url_kwarg = "booking_id"
    success_url = '/rooms/'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.room.hotel.owner != request.user and self.object.user != request.user:
            return self.handle_no_permission()

        overlapping_bookings = self.object.room.bookings.filter(
            check_in__lt=self.object.check_in,
            check_out__gt=self.object.check_out
        )
        if overlapping_bookings.exists():
            return self.handle_have_overlapping()

        return super().dispatch(request, *args, **kwargs)

    def handle_have_overlapping(self):
        return render(self.request, 'error.html', {"message": f'Извините, в эти дни номер уже забронирован.'})

    def handle_no_permission(self):
        return render(self.request, 'error.html', {"message": f'Извините, но у вас нет доступа к Отелю "{self.object.room.hotel.name}".'})

class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = 'booking_delete.html'
    pk_url_kwarg = "booking_id"
    success_url = '/rooms/'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.room.hotel.owner != request.user and self.object.user != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return render(self.request, 'error.html', {"message": f'Извините, но у вас нет доступа к Отелю "{self.object.hotel.name}".'})

def users_last_month(request):
    one_month_ago = timezone.now() - timedelta(days=30)
    users_with_recent_bookings = Booking.objects.filter(check_out__gt=one_month_ago).values_list('user', flat=True).distinct()
    users = User.objects.filter(id__in=users_with_recent_bookings)

    return render(request, "users.html", {"users": users})

def reviews(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        raise Http404("Poll does not exist")
    return render(request, "reviews.html", {"reviews": room.reviews.all(), 'room_number': room.number, 'hotel_name': room.hotel.name})


@login_required(login_url='/login/')
def review_create(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        raise Http404("Poll does not exist")
    user = request.user
    context = {}
    form = ReviewCreateForm(request.POST or None)
    if form.is_valid():
        hotel = form.save(commit=False)
        hotel.user = user
        hotel.room = room
        form.save()
        return redirect("/bookings/")
    context['form'] = form
    context['room'] = room
    return render(request, "review_create.html", context)