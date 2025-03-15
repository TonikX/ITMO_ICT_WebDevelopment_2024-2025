from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DeleteView, UpdateView
from django.http import HttpResponseRedirect
from .forms import UserRegistrationForm, ReservationForm, ReviewForm
from .models import Hotel, Room, Reservation
from datetime import datetime, timedelta

def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('rooms_list')  
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('rooms_list')
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('signin')

def rooms_list(request):
    rooms = Room.objects.all()
    return render(request, 'rooms_list.html', {'rooms': rooms})

def room_reviews(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    reviews = room.review_set.all() 
    return render(request, 'room_reviews.html', {'room': room, 'reviews': reviews})

@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.room = room
            reservation.save()
            return redirect('user_bookings')
    else:
        form = ReservationForm()
    return render(request, 'book_room.html', {'room': room, 'form': form})

@login_required
def write_review(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reservation = reservation
            review.save()
            return redirect('user_bookings')
    else:
        form = ReviewForm()
    return render(request, 'write_review.html', {'form': form, 'reservation': reservation})

@login_required
def user_bookings(request):
    bookings = Reservation.objects.filter(user=request.user)
    return render(request, 'user_bookings.html', {'bookings': bookings})

def monthly_clients(request):
    last_month = datetime.now() - timedelta(days=30)
    clients = set(Reservation.objects.filter(start_date__gte=last_month).values_list('user', flat=True))
    return render(request, 'monthly_clients.html', {'clients': clients})

class HotelListView(ListView):
    model = Hotel
    template_name = "hotel_list.html"
    context_object_name = "hotels"

class BookingDeleteView(DeleteView):
    model = Reservation
    success_url = "/user_bookings/" 

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

class BookingUpdateView(UpdateView):
    model = Reservation
    fields = ['start_date', 'end_date']
    template_name_suffix = '_update_form'
    success_url = "/user_bookings/" 

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)
