from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Flight, Reservation, Review
from .forms import ReservationForm, ReviewForm


@login_required
def flight_list(request):
    flights = Flight.objects.all()
    return render(request, 'flights/flight_list.html', {'flights': flights})


@login_required
def reserve_seat(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.flight = flight
            reservation.save()
            return redirect('flight_list')
    else:
        form = ReservationForm()
    return render(request, 'flights/reserve_seat.html', {'form': form, 'flight': flight})


@login_required
def flight_reviews(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    reviews = Review.objects.filter(flight=flight)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.flight = flight
            review.save()
            return redirect('flight_reviews', flight_id=flight_id)
    else:
        form = ReviewForm()
    return render(request, 'flights/flight_reviews.html', {'flight': flight, 'reviews': reviews, 'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('flight_list')
    else:
        form = UserCreationForm()
    return render(request, 'flights/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('flight_list')
    else:
        form = AuthenticationForm()
    return render(request, 'flights/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def add_review(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.flight = flight
            review.save()
            return redirect('flight_reviews', flight_id=flight_id)
    else:
        form = ReviewForm()
    return render(request, 'flights/add_review.html', {'form': form, 'flight': flight})
