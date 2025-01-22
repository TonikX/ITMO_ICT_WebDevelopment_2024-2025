from django.core.exceptions import PermissionDenied
from django.db.models import Subquery
from django.contrib.auth import login, authenticate, logout
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin


def is_administrator(user):
    return user.is_staff


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print(request.POST)
        print(form.errors)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('flights')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('flights')
            else:
                return render(request, 'user/login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = CustomAuthenticationForm()

        return render(request, 'user/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def flight_list(request):
    query = request.GET.get('q', '')

    flights = Flight.objects.all().order_by('departure')

    if query:
        flights = flights.filter(
            Q(flight_number__icontains=query) |
            Q(airline__icontains=query) |
            Q(origin__icontains=query) |
            Q(destination__icontains=query) |
            Q(departure__icontains=query) |
            Q(arrival__icontains=query) |
            Q(type__icontains=query) |
            Q(gate_number__icontains=query)
        )

    paginator = Paginator(flights, 4)  # 4 полёта на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'flights/flights.html', {
        'flights': page_obj,
        'query': query,
    })

def reservation_list(request):
    reservations = Reservation.objects.filter(user=request.user)

    # Если бронирований нет, передаем пустой flight
    flight = reservations.first().flight if reservations.exists() else None

    return render(request, 'reservations/reservations.html', {
        'reservations': reservations,
        'flight': flight,  # Теперь flight всегда есть в контексте
    })

def profile_view(request):
    return render(request, 'user/profile.html')

class FlightDetailView(LoginRequiredMixin, DetailView):
    model = Flight
    template_name = 'flights/flight.html'
    context_object_name = 'flight'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        flight = self.get_object()

        available_seats = Seat.objects.filter(flight=flight, is_reserved=False)
        reviews = Review.objects.filter(flight=flight)
        passengers = Passenger.objects.filter(flight=flight)

        context['reviews'] = reviews
        context['available_seats'] = available_seats
        context['passengers'] = passengers

        return context


@login_required
@user_passes_test(is_administrator)
def reservations_list(request, flight_pk):
    flight = get_object_or_404(Flight, pk=flight_pk)

    occupied_seat_ids = Passenger.objects.values('seat')
    reservations = Reservation.objects.filter(flight=flight).exclude(seat__in=Subquery(occupied_seat_ids))

    return render(request, 'reservations/reservations.html', {
        'flight': flight,
        'reservations': reservations,
    })

@login_required
@user_passes_test(is_administrator)
def passenger_list(request, flight_pk):
    flight = get_object_or_404(Flight, pk=flight_pk)
    passengers = Passenger.objects.filter(flight=flight)

    return render(request, 'flights/passengers.html', {
        'passengers': passengers,
        'flight': flight,
    })


@login_required
def submit_review(request, flight_pk):
    flight = get_object_or_404(Flight, pk=flight_pk)
    print("User:", request.user)
    print("Flight ID:", flight_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, user=request.user, flight=flight)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.flight = flight
            review.save()
            return redirect('flight_detail', pk=flight_pk)
    else:
        form = ReviewForm(user=request.user, flight=flight)

    return render(request, 'reviews/submit_review.html', {'form': form, 'flight': flight})


@login_required
@user_passes_test(is_administrator)
def register_passenger(request, reservation_pk):
    reservation = get_object_or_404(Reservation, pk=reservation_pk)
    passenger = Passenger(flight=reservation.flight,
                          seat=reservation.seat,
                          first_name=reservation.first_name,
                          last_name=reservation.last_name)
    if request.method == 'POST':
        form = RegisterPassengerForm(request.POST, instance=passenger)
        if form.is_valid():
            passenger.ticket_number = form.instance.ticket_number
            print("Savin passenger" + passenger.last_name)
            passenger.save()
            return redirect('reservations_list', flight_pk=reservation.flight.pk)
    else:
        form = RegisterPassengerForm(instance=passenger)

    return render(request, 'flights/register_passenger.html', {'form': form, 'reservation': reservation})


@login_required
def submit_reservation(request, flight_pk, seat_pk):
    flight = get_object_or_404(Flight, pk=flight_pk)
    seat = get_object_or_404(Seat, pk=seat_pk)

    if request.method == 'POST':
        form = ReservationForm(request.POST, user=request.user, flight=flight, seat=seat)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.flight = flight
            reservation.seat = seat
            seat.is_reserved = True
            seat.save()
            reservation.save()
            return redirect('flight_detail', pk=flight_pk)
    else:
        form = ReservationForm(user=request.user, flight=flight, seat=seat)

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

    if request.method == 'POST':
        form = EditReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('user_reservations')
    else:
        form = EditReservationForm(instance=reservation)

    return render(request, 'reservations/edit_reservation.html', {'form': form, 'reservation': reservation})


@login_required
def delete_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)

    if reservation.user != request.user:
        raise PermissionDenied("You do not have permission to delete this reservation.")

    if request.method == 'POST':
        if reservation.seat:
            seat = reservation.seat
            print(f"Deleting reservation for seat number: {seat.seat_number}, current status: {seat.is_reserved}")
            seat.is_reserved = False
            seat.save()

        reservation.delete()

        return redirect('user_reservations')

    return render(request, 'reservations/delete_reservation.html', {'reservation': reservation})


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user/profile.html'
    context_object_name = 'user'

    def get_object(self, **kwargs):
        return self.request.user
