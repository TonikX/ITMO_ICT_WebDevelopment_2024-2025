from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Flight, Reservation, Review
from .forms import ReservationForm, ReviewForm

def flight_list(request):
    flights = Flight.objects.all()
    return render(request, 'flight_list.html', {'flights': flights})

def flight_detail(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    reservations = Reservation.objects.filter(flight=flight)
    reviews = Review.objects.filter(flight=flight)
    return render(request, 'flight_detail.html', {
        'flight': flight, 'reservations': reservations, 'reviews': reviews
    })

@login_required
def create_reservation(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.flight = flight
            reservation.save()
            return redirect('flight_detail', flight_id=flight.id)
    else:
        form = ReservationForm()
    return render(request, 'create_reservation.html', {'form': form, 'flight': flight})

@login_required
def create_review(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.flight = flight
            review.save()
            return redirect('flight_detail', flight_id=flight.id)
    else:
        form = ReviewForm()
    return render(request, 'create_review.html', {'form': form, 'flight': flight})
