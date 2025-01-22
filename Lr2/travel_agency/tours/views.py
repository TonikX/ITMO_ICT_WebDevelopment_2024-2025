from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .forms import RegisterForm, ReservationForm, ReviewForm
from .models import Tour, Reservation


def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        new_user = form.save()
        login(request, new_user)
        return redirect('tours:tour_list')
    return render(request, 'tours/register.html', {'form': form})


def tour_list(request):
    tours = Tour.objects.all()
    user_reservations = []
    if request.user.is_authenticated:
        user_reservations = Reservation.objects.filter(user=request.user).values_list('tour_id', flat=True)
    context = {
        'tours': tours,
        'reserved_tours': user_reservations,
    }
    return render(request, 'tours/tour_list.html', context)


@login_required
def reserve_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if Reservation.objects.filter(tour=tour, user=request.user).exists():
        messages.info(request, "Этот тур уже забронирован вами.")
        return redirect('tours:tour_detail', tour_id=tour.id)

    if request.method == 'POST':
        Reservation.objects.create(tour=tour, user=request.user)
        messages.success(request, f"Тур '{tour.name}' успешно забронирован!")
        return redirect('tours:tour_detail', tour_id=tour.id)

    return render(request, 'tours/tour_booking.html', {'tour': tour})


@login_required
def my_reservations(request):
    user_reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'tours/my_bookings.html', {'reservations': user_reservations})


@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, "Бронирование успешно отменено.")
        return redirect('tours:my_reservations')
    return render(request, 'tours/cancel_booking.html', {'reservation': reservation})


@login_required
def add_review(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    form = ReviewForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        review = form.save(commit=False)
        review.tour = tour
        review.user = request.user
        review.save()
        messages.success(request, "Ваш отзыв добавлен.")
        return redirect('tours:tour_detail', tour_id=tour.id)
    return render(request, 'tours/feedback.html', {'form': form, 'tour': tour})


def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    reviews = tour.reviews.all().order_by('-review_date')
    user_reserved = request.user.is_authenticated and Reservation.objects.filter(tour=tour, user=request.user).exists()
    context = {
        'tour': tour,
        'reviews': reviews,
        'reservation_exists': user_reserved,
    }
    return render(request, 'tours/tour_detail.html', context)


def sold_tours_by_country(request):
    tour_sales = Tour.objects.annotate(total_sold=Count('reservations')).filter(total_sold__gt=0).values('country',
                                                                                                         'total_sold')
    return render(request, 'tours/sales_by_country.html', {'data': tour_sales})