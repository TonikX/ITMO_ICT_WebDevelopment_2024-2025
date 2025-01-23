from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404

from .models import Flight, Review


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('flight_list')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def flight_list(request):
    flights = Flight.objects.all()
    return render(request, 'flight_list.html', {'flights': flights})


def add_review(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    if request.method == 'POST':
        rating = request.POST['rating']
        comment_text = request.POST['comment_text']
        Review.objects.create(flight=flight, user=request.user, rating=rating, comment_text=comment_text)
        return redirect('flight_list')
    return render(request, 'add_review.html', {'flight': flight})


@login_required
def flight_details(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)

    if is_user_staff := request.user.is_staff:
        passengers = Reservation.objects.filter(flight=flight)

    reviews = Review.objects.filter(flight=flight)
    user_reservation = None
    if request.user.is_authenticated:
        user_reservation = Reservation.objects.filter(flight=flight, user=request.user).first()

    return render(request, 'flight_details.html', {
        'flight': flight,
        'passengers': passengers if is_user_staff else None,
        'is_staff': is_user_staff,
        'reviews': reviews,
        'user_reservation': user_reservation,
    })


# views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Reservation


class MyReservationsView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'my_reservations.html'
    context_object_name = 'reservations'
    paginate_by = 10  # Number of reservations per page

    def get_queryset(self):
        queryset = Reservation.objects.filter(user=self.request.user).order_by('-created_at')

        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                flight__flight_number__icontains=query
            ) | queryset.filter(
                flight__airline__icontains=query
            )

        return queryset


def edit_reservation(request, reservation_id):
    """Edit a specific reservation for the logged-in user."""
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        seat_number = request.POST.get('seat_number')
        reservation.seat_number = seat_number
        reservation.save()
        return redirect('my_reservations')
    return render(request, 'edit_reservation.html', {'reservation': reservation})


@login_required
def delete_reservation(request, reservation_id):
    """Delete a specific reservation for the logged-in user."""
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        reservation.delete()
        return redirect('my_reservations')
    return render(request, 'delete_reservation.html', {'reservation': reservation})


@login_required
def reserve_seat(request, flight_id):
    """Reserve a seat on a specific flight for the logged-in user."""
    flight = get_object_or_404(Flight, id=flight_id)
    if request.method == 'POST':
        seat_number = request.POST.get('seat_number')
        # Check if the seat is already reserved by another user on this flight
        if Reservation.objects.filter(flight=flight, seat_number=seat_number).exists():
            return render(request, 'reserve_seat.html', {
                'flight': flight,
                'error': "This seat is already reserved. Please choose another seat."
            })
        Reservation.objects.create(user=request.user, flight=flight, seat_number=seat_number)
        return redirect('my_reservations')
    return render(request, 'reserve_seat.html', {'flight': flight})


class FlightListView(ListView):
    model = Flight
    template_name = 'flight_list.html'
    context_object_name = 'flights'
    paginate_by = 2

    def get_queryset(self):
        queryset = Flight.objects.all().order_by('departure')

        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                flight_number__icontains=query
            ) | queryset.filter(
                airline__icontains=query
            )

        return queryset
