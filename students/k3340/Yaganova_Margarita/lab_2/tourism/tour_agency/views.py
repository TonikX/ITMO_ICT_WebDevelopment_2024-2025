from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth import login, authenticate
from .forms import BookingForm, TouristRegistrationForm, ReviewForm, \
    CountrySelectionForm
from django.db.models import Q


def tour_list(request):
    tours = Tour.objects.all()
    return render(request, 'tour_list.html', {'tours': tours})


def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    reviews = Review.objects.filter(tour=tour)
    country = Country.objects.filter(tour=tour)[0]
    return render(request, 'tour_detail.html',
                  {'tour': tour, 'reviews': reviews, 'country': country})


def booking(request, tour_id):
    if not request.user.is_authenticated:
        return redirect('login')
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            tour_booking = form.save(commit=False)
            tour_booking.tourist = request.user
            tour_booking.status = 'W'
            tour_booking.tour_id = tour.pk
            tour_booking.save()
            return redirect('account')
    else:
        form = BookingForm(initial={'tour_id': tour_id}, tour_id=tour_id)
    return render(request, 'booking.html', {'form': form})


class TouristLoginView(LoginView):
    template_name = 'registration/login.html'


class TouristLogoutView(LogoutView):
    template_name = 'registration/logout.html'


def register(request):
    if request.method == 'POST':
        form = TouristRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('account')
    else:
        form = TouristRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def account(request):
    bookings = TourBooking.objects.filter(tourist=request.user)
    return render(request, 'registration/account.html', {'bookings': bookings})


def edit_tour(request, booking_id):
    booking = get_object_or_404(TourBooking, id=booking_id)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            tour_booking = form.save(commit=False)
            tour_booking.status = 'W'
            tour_booking.save()
            return redirect('account')
    else:
        form = BookingForm(instance=booking, initial={'tour_id': booking.tour.pk},
                           tour_id=booking.tour.pk)
    return render(request, 'edit_tour.html', {'form': form, 'tour': booking})


def review(request, tour_id, booking_id):
    if not request.user.is_authenticated:
        return redirect('login')
    tour = get_object_or_404(Tour, pk=tour_id)
    booking = get_object_or_404(TourBooking, pk=booking_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.tourist = request.user
            review.tour = tour
            review.booking = booking
            review.save()
            return redirect('account')
    else:
        form = ReviewForm()
    return render(request, 'review.html', {'form': form})


def delete_booking(request, booking_id):
    booking = TourBooking.objects.get(pk=booking_id)
    if request.method == 'POST':
        booking.delete()
        return redirect('account')
    return redirect('account')


def tour_table(request):
    country_form = CountrySelectionForm(request.GET)

    if country_form.is_valid():
        country = country_form.cleaned_data['country']
        tours = Tour.objects.filter(country=country)
        completed_bookings = TourBooking.objects.filter(Q(tour__in=tours),
                                                        status="D")
    else:
        completed_bookings = TourBooking.objects.filter(status="D")
    return render(request, 'tour_table.html', {'bookings': completed_bookings,
                                               'country_form': country_form})
