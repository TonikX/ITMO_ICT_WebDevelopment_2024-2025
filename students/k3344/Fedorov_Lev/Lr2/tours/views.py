from decimal import Decimal
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserForm, TravelAgencyForm, ReviewForm, TourForm, BookingForm
from .models import Tour, Country, Review, Booking


def tour_list(request):
    query = request.GET.get('q')
    if query:
        tours = Tour.objects.prefetch_related('reviews').filter(country__name__icontains=query)
    else:
        tours = Tour.objects.prefetch_related('reviews').all()

    paginator = Paginator(tours, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for tour in page_obj:
        tour.user_has_booking = tour.bookings.filter(
            user=request.user).exists() if request.user.is_authenticated else False

    return render(request, 'tour_list.html', {'page_obj': page_obj, 'query': query})


@login_required
def user_dashboard(request):
    reviews = Review.objects.filter(user=request.user)
    tours = Tour.objects.all()
    bookings = Booking.objects.filter(user=request.user)
    confirmed_tours = [booking.tour.id for booking in bookings if booking.is_confirmed]
    return render(request, 'user_dashboard.html', {
        'reviews': reviews,
        'tours': tours,
        'bookings': bookings,
        'confirmed_tours': confirmed_tours
    })

@login_required
def add_review(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if not Booking.objects.filter(tour=tour, user=request.user, is_confirmed=True).exists():
        return render(request, 'add_review.html', {'error': 'You can only leave a review after your booking is confirmed.'})

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.tour = tour
            review.save()
            return redirect('user_dashboard')
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'tour': tour})


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')
    else:
        form = ReviewForm(instance=review)
    return render(request, 'edit_review.html', {'form': form})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        review.delete()
        return redirect('user_dashboard')
    return render(request, 'delete_review.html', {'review': review})


def register_reviewer(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tour_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def register_agency(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        agency_form = TravelAgencyForm(request.POST)
        if user_form.is_valid() and agency_form.is_valid():
            user = user_form.save()
            agency = agency_form.save(commit=False)
            agency.user = user
            agency.save()
            login(request, user)
            return redirect('agency_dashboard')
    else:
        user_form = UserForm()
        agency_form = TravelAgencyForm()
    return render(request, 'register_agency.html', {'user_form': user_form, 'agency_form': agency_form})


@login_required
def agency_dashboard(request):
    if not hasattr(request.user, 'agency'):
        return render(request, 'agency_dashboard.html', {'message': 'Ваших туров пока что нету. Добавьте новый тур.'})
    tours = request.user.agency.tours.all()
    if not tours:
        return render(request, 'agency_dashboard.html', {'message': 'Ваших туров пока что нету. Добавьте новый тур.'})
    return render(request, 'agency_dashboard.html', {'tours': tours})


@login_required
def create_tour(request):
    if not hasattr(request.user, 'agency'):
        return redirect('tour_list')
    if request.method == 'POST':
        form = TourForm(request.POST)
        if form.is_valid():
            tour = form.save(commit=False)
            tour.agency = request.user.agency
            tour.price = Decimal(form.cleaned_data['price'])
            tour.save()
            return redirect('agency_dashboard')
    else:
        form = TourForm()
    return render(request, 'create_tour.html', {'form': form})


@login_required
def edit_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id, agency=request.user.agency)
    if request.method == 'POST':
        form = TourForm(request.POST, instance=tour)
        if form.is_valid():
            tour = form.save(commit=False)
            tour.price = Decimal(form.cleaned_data['price'])
            tour.save()
            return redirect('agency_dashboard')
    else:
        form = TourForm(instance=tour)
    return render(request, 'edit_tour.html', {'form': form})


@login_required
def delete_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id, agency=request.user.agency)
    if request.method == 'POST':
        tour.delete()
        return redirect('agency_dashboard')
    return render(request, 'delete_tour.html', {'tour': tour})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if hasattr(user, 'agency'):
                    return redirect('agency_dashboard')
                elif hasattr(user, 'reviewer'):
                    return redirect('reviewer_dashboard')
                else:
                    return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def book_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if Booking.objects.filter(user=request.user, tour=tour).exists():
        messages.error(request, 'You have already reserved this tour.')
    else:
        Booking.objects.create(tour=tour, user=request.user)
        messages.success(request, 'Tour reserved successfully.')
    return redirect('user_dashboard')


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.delete()
        return redirect('user_dashboard')
    return render(request, 'cancel_booking.html', {'booking': booking})


@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'edit_booking.html', {'form': form})


@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.delete()
        return redirect('user_dashboard')
    return render(request, 'delete_booking.html', {'booking': booking})


@staff_member_required
def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.confirmed = True
        booking.save()
        return redirect('admin:index')
    return render(request, 'confirm_booking.html', {'booking': booking})


def sold_tours_by_country(request):
    sort = request.GET.get('sort', 'name')
    if sort == 'name':
        countries = Country.objects.all().order_by('name')
    elif sort == 'tours_asc':
        countries = Country.objects.all().annotate(tour_count=Count('tours')).order_by('tour_count')
    elif sort == 'tours_desc':
        countries = Country.objects.all().annotate(tour_count=Count('tours')).order_by('-tour_count')
    else:
        countries = Country.objects.all()

    paginator = Paginator(countries, 10)  # Show 10 countries per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'sold_tours_by_country.html', {'page_obj': page_obj, 'sort': sort})


def user_logout(request):
    logout(request)
    return redirect('tour_list')


def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    return render(request, 'tour_detail.html', {'tour': tour})
