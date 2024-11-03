from django.core.exceptions import PermissionDenied
from django.db.models import Subquery
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.views.generic import CreateView, ListView, DetailView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def is_administrator(user):
    return user.is_staff


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registration
            return redirect('flights')  # Redirect to home or another page after registration
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
                return redirect('flights')  # Redirect to a success page
            else:
                return render(request, 'user/login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = CustomAuthenticationForm()

        return render(request, 'user/login.html', {'form': form})


@login_required  # Ensure that only logged-in users can access this view
def logout_view(request):
    logout(request)  # Log out the user
    return redirect('flights')  # Redirect to the home page or any other page after logging out


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

        available_seats = Seat.objects.filter(flight=flight, is_reserved=False)
        reviews = Review.objects.filter(flight=flight)
        context['reviews'] = reviews
        context['available_seats'] = available_seats

        return context


@login_required
@user_passes_test(is_administrator)
def reservations_list(request, flight_pk):
    flight = get_object_or_404(Flight, pk=flight_pk)

    # reservations = Reservation.objects.filter(flight=flight)

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
    flight = get_object_or_404(Flight, pk=flight_pk)  # Get flight by number
    print("User:", request.user)
    print("Flight ID:", flight_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, user=request.user, flight=flight)
        if form.is_valid():
            review = form.save(commit=False)  # Create review instance without saving to DB yet
            review.user = request.user  # Set user from request
            review.flight = flight  # Set flight from URL
            review.save()  # Save review to DB
            return redirect('flight_detail', pk=flight_pk)  # Redirect after saving
    else:
        form = ReviewForm(user=request.user, flight=flight)

    return render(request, 'reviews/submit_review.html', {'form': form, 'flight': flight})


@login_required
@user_passes_test(is_administrator)
def register_passenger(request, reservation_pk):
    reservation = get_object_or_404(Reservation, pk=reservation_pk)  # Get the reservation by primary key
    passenger = Passenger(flight=reservation.flight,  # Set flight from reservation
                          seat=reservation.seat,  # Set seat from reservation
                          first_name=reservation.first_name,  # Set first name from reservation
                          last_name=reservation.last_name)
    if request.method == 'POST':
        # form = RegisterPassengerForm(request.POST, reservation=reservation, )
        form = RegisterPassengerForm(request.POST, instance=passenger)
        if form.is_valid():
            # passenger = form.save(commit=False)
            # passenger.flight = reservation.flight
            # passenger.seat = reservation.seat
            # passenger.first_name = reservation.first_name
            # passenger.last_name = reservation.last_name
            passenger.ticket_number = form.instance.ticket_number
            print("Savin passenger" + passenger.last_name)
            passenger.save()
            # form.save()  # Save the new passenger record
            return redirect('reservations_list', flight_pk=reservation.flight.pk)  # Redirect after registration
    else:
        form = RegisterPassengerForm(instance=passenger)  # Pre-fill the form with existing data

    return render(request, 'flights/register_passenger.html', {'form': form, 'reservation': reservation})


@login_required
def submit_reservation(request, flight_pk, seat_pk):
    flight = get_object_or_404(Flight, pk=flight_pk)  # Get flight by number
    seat = get_object_or_404(Seat, pk=seat_pk)  # Get seat by ID

    if request.method == 'POST':
        form = ReservationForm(request.POST, user=request.user, flight=flight, seat=seat)
        if form.is_valid():
            reservation = form.save(commit=False)  # Create reservation instance without saving to DB yet
            reservation.user = request.user  # Set user from request (already set in __init__)
            reservation.flight = flight  # Set flight from URL (already set in __init__)
            reservation.seat = seat  # Set seat from URL (already set in __init__)
            seat.is_reserved = True
            seat.save()
            reservation.save()  # Save reservation to DB
            return redirect('flight_detail', pk=flight_pk)  # Redirect after saving
    else:
        form = ReservationForm(user=request.user, flight=flight, seat=seat)

    return render(request, 'reservations/submit_reservation.html', {'form': form, 'flight': flight, 'seat': seat})


class UserReservationsView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'reservations/reservations.html'  # Template to render
    context_object_name = 'reservations'  # Name of the context variable for reservations

    def get_queryset(self):
        # Return all reservations for the current user
        return Reservation.objects.filter(user=self.request.user)


@login_required
def edit_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)  # Get the reservation by primary key

    if request.method == 'POST':
        form = EditReservationForm(request.POST, instance=reservation)  # Bind form to existing reservation
        if form.is_valid():
            form.save()  # Save changes to first_name and last_name
            return redirect('user_reservations')  # Redirect to user's reservations page after saving
    else:
        form = EditReservationForm(instance=reservation)  # Pre-fill the form with existing data

    return render(request, 'reservations/edit_reservation.html', {'form': form, 'reservation': reservation})


@login_required  # Ensure that only logged-in users can access this view
def delete_reservation(request, pk):
    # Get the reservation object or return a 404 if not found
    reservation = get_object_or_404(Reservation, pk=pk)

    # Check if the reservation belongs to the logged-in user
    if reservation.user != request.user:
        raise PermissionDenied("You do not have permission to delete this reservation.")

    # Handle POST request for deletion
    if request.method == 'POST':
        # Assuming each reservation is linked to a seat
        if reservation.seat:
            seat = reservation.seat
            print(f"Deleting reservation for seat number: {seat.seat_number}, current status: {seat.is_reserved}")
            seat.is_reserved = False  # Set is_reserved to False
            seat.save()  # Save the seat instance

        # Delete the reservation
        reservation.delete()

        # Redirect to user's reservations page after deletion
        return redirect('user_reservations')

    # Render confirmation template for GET requests
    return render(request, 'reservations/delete_reservation.html', {'reservation': reservation})


# class ReservationDeleteView(LoginRequiredMixin, DeleteView):
#     model = Reservation
#     template_name = 'reservations/delete_reservation.html'  # Template to confirm deletion
#     success_url = reverse_lazy('user_reservations')  # Redirect to user's reservations after deletion
#
#     def get_object(self, queryset=None):
#         # Override to ensure that the user can only delete their own reservations
#         obj = super().get_object(queryset)
#         if obj.user != self.request.user:
#             raise PermissionDenied("You do not have permission to delete this reservation.")
#         return obj
#
#     def delete(self, request, *args, **kwargs):
#         # Get the reservation object
#         reservation = self.get_object()
#
#         # Assuming each reservation is linked to a seat
#         if reservation.seat:
#             seat = reservation.seat
#             print(f"Deleting reservation for seat number: {seat.seat_number}, current status: {seat.is_reserved}")
#             seat.is_reserved = False
#             seat.save()
#         else:
#             print("No associated seat found for this reservation.")
#         # Call the superclass's delete method to delete the reservation
#         return super().delete(request, *args, **kwargs)


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user/profile.html'  # Specify your template here
    context_object_name = 'user'  # This will be used in the template to refer to the user object

    def get_object(self):
        return self.request.user  # Return the currently logged-in user

# def seat_list(request, flight_id):  # should be different for admin
#     flight = get_object_or_404(Flight, pk=flight_id)
#     seats = Seat.objects.filter(flight=flight, is_reserved=False)
#     return render(request, 'seat_list.html', {'flight': flight, 'seats': seats})
#
#
# class CreateFlightView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
#     model = Flight
#     form_class = FlightForm
#     template_name = 'create_flight.html'
#     success_url = reverse_lazy('flight_list')
#
#     def test_func(self):
#         return self.request.user.is_staff
#
#
#
#
#
# @login_required
# def reserve_seat(request, seat_id):  # добавить внесение имени и фамилии
#     seat = get_object_or_404(Seat, pk=seat_id, is_reserved=False)
#     if request.method == 'POST':
#         seat.is_reserved = True
#         seat.save()
#         reservation = Reservation(user=request.user, flight=seat.flight, seat=seat)
#         reservation.save()
#         return redirect('reservation_detail', pk=reservation.pk)
#     else:
#         return render(request, 'reserve_seat.html', {'seat': seat})
#
#
# @login_required
# def edit_reservation(request, reservation_id):
#     reservation = get_object_or_404(Reservation, pk=reservation_id, user=request.user)
#     if request.method == 'POST':
#         form = ReservationForm(request.POST, instance=reservation)
#         if form.is_valid():
#             form.save()
#             return redirect('reservation_detail', pk=reservation.pk)
#     else:
#         form = ReservationForm(instance=reservation)
#     return render(request, 'edit_reservation.html', {'form': form, 'reservation': reservation})
#
#
# @login_required
# def delete_reservation(request, reservation_id):
#     reservation = get_object_or_404(Reservation, pk=reservation_id, user=request.user)
#     reservation.seat.is_reserved = False
#     reservation.seat.save()
#     reservation.delete()
#     return redirect('reservation_list')
#
#
# @login_required
# def reservation_list(request):
#     reservations = Reservation.objects.filter(user=request.user)
#     return render(request, 'flights.html', {'flights': reservations})
#
#
# @login_required
# @user_passes_test(is_administrator)
# def admin_view(request):
#     # This view is only accessible to administrators
#     pass
#
#
# class SignUp(CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'signup.html'
#
#
# @login_required
# @user_passes_test(is_administrator)
# def create_flight(request):
#     if request.method == 'POST':
#         form = FlightForm(request.POST)
#         if form.is_valid():
#             flight = form.save()
#             return redirect('flight_detail', pk=flight.pk)
#     else:
#         form = FlightForm()
#     return render(request, 'create_flight.html', {'form': form})
#
#
# @login_required
# @user_passes_test(is_administrator)
# def seat_list(request, flight_id):
#     flight = get_object_or_404(Flight, pk=flight_id)
#     seats = Seat.objects.filter(flight=flight)
#     seat_data = []
#     for seat in seats:
#         reservation = Reservation.objects.filter(seat=seat).first()
#         passenger = Passenger.objects.filter(seat=seat).first()
#         if reservation:
#             status = 'Reserved'
#             details_url = f'/reservations/{reservation.pk}/'
#         elif passenger:
#             status = 'Registered'
#             details_url = f'/passengers/{passenger.pk}/'
#         else:
#             status = 'Available'
#             details_url = None
#         seat_data.append({'seat': seat, 'status': status, 'details_url': details_url})
#     return render(request, 'seat_list.html', {'flight': flight, 'seat_data': seat_data})
#
#
# @login_required
# @user_passes_test(is_administrator)
# def register_passenger(request, flight_id):
#     flight = get_object_or_404(Flight, pk=flight_id)
#     if request.method == 'POST':
#         form = PassengerForm(request.POST)
#         if form.is_valid():
#             passenger = form.save(commit=False)
#             passenger.flight = flight
#             passenger.save()
#             return redirect('flight_detail', pk=flight.pk)
#     else:
#         form = PassengerForm()
#     return render(request, 'register_passenger.html', {'form': form, 'flight': flight})
#
#
# @login_required
# def create_review(request, flight_id):
#     flight = Flight.objects.get(id=flight_id)
#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.user = request.user
#             review.flight = flight
#             review.save()
#             return redirect('flight_detail', pk=flight.pk)
#     else:
#         form = ReviewForm()
#     return render(request, 'create_review.html', {'form': form, 'flight': flight})
#
#
# class UserReviewsView(LoginRequiredMixin, ListView):
#     model = Review
#     template_name = 'user_reviews.html'
#
#     def get_queryset(self):
#         return Review.objects.filter(user=self.request.user)
#
#
# class FlightReviewsView(ListView):
#     model = Review
#     template_name = 'flight_reviews.html'
#
#     def get_queryset(self):
#         flight_id = self.kwargs['flight_id']
#         return Review.objects.filter(flight_id=flight_id)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['flight'] = Flight.objects.get(id=self.kwargs['flight_id'])
#         return context
