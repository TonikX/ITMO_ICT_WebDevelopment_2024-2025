from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, ReservationForm, ReviewForm
from .models import Flight, Reservation
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    reservations = request.user.reservations.all()
    context = {
        'user': request.user,
        'reservations': reservations,
    }
    return render(request, 'profile.html', context)


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
            return redirect('profile')  # Redirect to the profile page after reservation
    else:
        form = ReservationForm()

    return render(request, 'reserve_seat.html', {'form': form, 'flight': flight})

@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    reservation.delete()
    return redirect('profile')

@login_required
def flight_passengers(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    passengers = flight.reservations.prefetch_related('passengers').all()
    return render(request, 'flights/flight_passengers.html', {'flight': flight, 'passengers': passengers})



def home(request):
    return render(request, 'home.html')



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def flight_list(request):
    flights = Flight.objects.all()
    return render(request, 'flights/flight_list.html', {'flights': flights})


def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('flight_list')  # Redirect after edit
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'flights/edit_reservation.html', {'form': form})


def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        reservation.delete()
        return redirect('flight_list')  # Redirect after deletion
    return render(request, 'flights/delete_reservation.html', {'reservation': reservation})


def flight_passengers(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    passengers = flight.reservations.values('passengers__first_name', 'passengers__last_name', 'passengers__ticket_number')
    return render(request, 'flights/flight_passengers.html', {'flight': flight, 'passengers': passengers})


def add_review(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.flight = flight
            review.review_date = flight.departure_time.date()  # Assuming review date is flight date
            review.save()
            return redirect('flight_list')  # Redirect after review
    else:
        form = ReviewForm()
    return render(request, 'flights/add_review.html', {'form': form, 'flight': flight})

def flight_reviews(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    reviews = flight.reviews.all()
    return render(request, 'flights/flight_reviews.html', {'flight': flight, 'reviews': reviews})
