from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.db.models import Avg
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, BookingForm, ReviewForm
from .models import Flight, Booking, Review, User


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            passport_number = form.cleaned_data.get('passport_number')
            raw_password = form.cleaned_data.get('password1')

            # Authenticate the user with passport_number and raw_password
            user = authenticate(passport_number=passport_number, password=raw_password)

            if user is not None:  # Check if authentication was successful
                login(request, user)  # Log the user in
                return redirect('flights')  # Redirect to the flights page
            else:
                form.add_error(None, 'Authentication failed. Please check your credentials.')
        else:
            # This handles the case where the form is not valid
            form.add_error(None, 'There was an error with your registration details.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})  # Render the form


class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = AuthenticationForm

    def get_success_url(self):
        return redirect('flights').url

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, error='Invalid passport number or password'))


def user_logout(request):
    logout(request)
    return redirect('flights')


class Flights(ListView):
    model = Flight
    template_name = 'flights.html'
    context_object_name = 'flights'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FlightInfoView(DetailView):
    model = Flight
    template_name = 'flight_info.html'
    context_object_name = 'flight'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['passengers'] = Booking.objects.filter(flight=self.object)
        mean_rating = Review.objects.filter(booking__flight=self.object).aggregate(Avg('rating'))['rating__avg']
        context['mean_rating'] = mean_rating

        return context


@login_required
def make_booking(request, pk):
    flight = get_object_or_404(Flight, pk=pk)
    if request.method == 'POST':
        booking_number = str(Booking.objects.count() + 1).zfill(3)
        Booking.objects.create(
            user=request.user,
            flight=flight,
            booking_number=booking_number
        )
        return redirect('bookings')
    else:
        return redirect('flight_info', pk=pk)


@login_required
def bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings.html', {'bookings': bookings})


@login_required
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        booking.delete()
        return redirect('bookings')
    return render(request, 'booking_delete.html', {'booking': booking})


@login_required
def review_create(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.create(
                booking=booking,
                text=form.cleaned_data['text'],
                rating=form.cleaned_data['rating']
            )
            return redirect('flight_info', pk=booking.flight.pk)
    else:
        form = ReviewForm()
    return render(request, 'review_form.html', {'form': form, 'booking': booking})
