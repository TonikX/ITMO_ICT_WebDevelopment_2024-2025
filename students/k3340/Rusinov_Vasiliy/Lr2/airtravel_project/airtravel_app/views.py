from django.core.exceptions import PermissionDenied
from django.db.models import Subquery
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def is_administrator(user):
    return user.is_staff


def register(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('flights')
    return render(request, 'user/register.html', {'form': form})


def login_view(request):
    form = CustomAuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user:
            login(request, user)
            return redirect('flights')
        return render(request, 'user/login.html', {'form': form, 'error': 'Invalid credentials'})
    return render(request, 'user/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('flights')


class FlightListView(ListView):
    model = Flight
    template_name = 'flights/flights.html'
    context_object_name = 'flights'

    def get_queryset(self):
        return Flight.objects.all()


class FlightDetailView(LoginRequiredMixin, DetailView):
    model = Flight
    template_name = 'flights/flight.html'
    context_object_name = 'flight'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        flight = self.get_object()
        context['reviews'] = Review.objects.filter(flight=flight)
        context['available_seats'] = Seat.objects.filter(flight=flight, is_reserved=False)
        return context


@login_required
@user_passes_test(is_administrator)
def reservations_list(request, flight_pk):
    flight = get_object_or_404(Flight, pk=flight_pk)
    occupied_seat_ids = Passenger.objects.values('seat')
    reservations = Reservation.objects.filter(flight=flight).exclude(seat__in=Subquery(occupied_seat_ids))
    return render(request, 'reservations/reservations.html', {'flight': flight, 'reservations': reservations})


@login_required
@user_passes_test(is_administrator)
def passenger_list(request, flight_pk):
    flight = get_object_or_404(Flight, pk=flight_pk)
    passengers = Passenger.objects.filter(flight=flight)
    return render(request, 'flights/passengers.html', {'passengers': passengers, 'flight': flight})


@login_required
def submit_review(request, flight_pk):
    flight = get_object_or_404(Flight, pk=flight_pk)
    form = ReviewForm(request.POST or None, user=request.user, flight=flight)
    if request.method == 'POST' and form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.flight = flight
        review.save()
        return redirect('flight_detail', pk=flight_pk)
    return render(request, 'reviews/submit_review.html', {'form': form, 'flight': flight})


@login_required
@user_passes_test(is_administrator)
def register_passenger(request, reservation_pk):
    reservation = get_object_or_404(Reservation, pk=reservation_pk)
    passenger = Passenger(flight=reservation.flight, seat=reservation.seat, first_name=reservation.first_name,
                          last_name=reservation.last_name)
    form = RegisterPassengerForm(request.POST or None, instance=passenger)
    if request.method == 'POST' and form.is_valid():
        passenger.ticket_number = form.instance.ticket_number
        passenger.save()
        return redirect('reservations_list', flight_pk=reservation.flight.pk)
    return render(request, 'flights/register_passenger.html', {'form': form, 'reservation': reservation})


@login_required
def submit_reservation(request, flight_pk, seat_pk):
    flight = get_object_or_404(Flight, pk=flight_pk)
    seat = get_object_or_404(Seat, pk=seat_pk)
    form = ReservationForm(request.POST or None, user=request.user, flight=flight, seat=seat)
    if request.method == 'POST' and form.is_valid():
        reservation = form.save(commit=False)
        reservation.user = request.user
        reservation.flight = flight
        reservation.seat = seat
        seat.is_reserved = True
        seat.save()
        reservation.save()
        return redirect('flight_detail', pk=flight_pk)
    return render(request, 'reservations/submit_reservation.html', {'form': form, 'flight': flight, 'seat': seat})


class UserReservationsView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'reservations/reservations.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


@login_required
def edit_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    form = EditReservationForm(request.POST or None, instance=reservation)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('user_reservations')
    return render(request, 'reservations/edit_reservation.html', {'form': form, 'reservation': reservation})


@login_required
def delete_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if reservation.user != request.user:
        raise PermissionDenied("You do not have permission to delete this reservation.")

    if request.method == 'POST':
        if reservation.seat:
            reservation.seat.is_reserved = False
            reservation.seat.save()
        reservation.delete()
        return redirect('user_reservations')
    return render(request, 'reservations/delete_reservation.html', {'reservation': reservation})


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user/profile.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user
