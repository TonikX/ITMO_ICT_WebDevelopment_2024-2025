from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, BookingForm, ReviewForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Flight, Booking, Review, User
from django.views.generic import ListView, DetailView

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            passport_number = form.cleaned_data.get('passport_number')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(passport_number=passport_number, password=raw_password)
            login(request, user)
            return redirect('flight_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        passport_number = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(passport_number=passport_number, password=password)
        if user is not None:
            login(request, user)
            return redirect('flight_list')
        else:
            form = AuthenticationForm(request, data=request.POST)
            return render(request, 'registration/login.html', {'form': form, 'error': 'Неверный номер паспорта или пароль'})
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('flight_list')

class FlightListView(ListView):
    model = Flight
    template_name = 'flight_list.html'
    context_object_name = 'flights'

class FlightDetailView(DetailView):
    model = Flight
    template_name = 'flight_detail.html'
    context_object_name = 'flight'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['passengers'] = Booking.objects.filter(flight=self.object)
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
        return redirect('booking_list')
    else:
        return redirect('flight_detail', pk=pk)

@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking_list.html', {'bookings': bookings})

@login_required
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        booking.delete()
        return redirect('booking_list')
    return render(request, 'booking_confirm_delete.html', {'booking': booking})

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
            return redirect('flight_detail', pk=booking.flight.pk)
    else:
        form = ReviewForm()
    return render(request, 'review_form.html', {'form': form, 'booking': booking})
