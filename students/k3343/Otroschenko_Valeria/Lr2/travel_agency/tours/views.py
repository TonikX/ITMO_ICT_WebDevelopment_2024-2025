from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import RegisterForm, ReservationForm, ReviewForm
from .models import Tour, Reservation, Review
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tours:tour_list')
        print(form.errors)
    else:
        form = RegisterForm()
    return render(request, 'tours/register.html', {'form': form})

def tour_list(request):
    #tours = Tour.objects.all()
    #return render(request, 'tours/tour_list.html', {'tours': tours})
    tours = Tour.objects.all()
    reserved_tours = []
    if request.user.is_authenticated:
        # Получаем ID туров, зарезервированных текущим пользователем
        reserved_tours = Reservation.objects.filter(user=request.user).values_list('tour_id', flat=True)
    return render(request, 'tours/tour_list.html', {
        'tours': tours,
        'reserved_tours': reserved_tours,
    })

@login_required
def reserve_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    # Проверка, уже зарезервировал ли пользователь этот тур
    reservation_exists = Reservation.objects.filter(tour=tour, user=request.user).exists()

    if reservation_exists:
        messages.warning(request, "Вы уже зарезервировали этот тур.")
        return redirect('tours:tour_detail', tour_id=tour.id)

    if request.method == 'POST':
        try:
            # Создаём резервацию
            reservation = Reservation.objects.create(tour=tour, user=request.user)
            messages.success(request, f"Вы успешно зарезервировали тур: {tour.name}")
            return redirect('tours:tour_detail', tour_id=tour.id)
        except Exception as e:
            messages.error(request, "Произошла ошибка при резервировании тура. Пожалуйста, попробуйте позже.")
            return redirect('tours:tour_detail', tour_id=tour.id)

    return render(request, 'tours/reserve_tour.html', {'tour': tour})

@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'tours/my_reservations.html', {'reservations': reservations})

@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        reservation.delete()
        return redirect('tours:my_reservations')
    return render(request, 'tours/delete_reservation.html', {'reservation': reservation})

@login_required
def add_review(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.tour = tour
            review.user = request.user
            review.save()
            return redirect('tours:tour_detail', tour_id=tour.id)
    else:
        form = ReviewForm()
    return render(request, 'tours/add_review.html', {'form': form, 'tour': tour})


def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    reviews = tour.reviews.all().order_by('-review_date')  # Предполагается, что related_name='reviews'

    # Проверяем, зарезервировал ли пользователь тур
    reservation_exists = False
    if request.user.is_authenticated:
        reservation_exists = Reservation.objects.filter(tour=tour, user=request.user).exists()

    return render(request, 'tours/tour_detail.html', {
        'tour': tour,
        'reviews': reviews,
        'reservation_exists': reservation_exists,
    })

def sold_tours_by_country(request):
    data = (
        Tour.objects.annotate(total_sold=Count('reservations'))
        .values('country', 'total_sold')
        .filter(total_sold__gt=0)  # Показываем только страны с продажами
    )
    return render(request, 'tours/sold_tours_by_country.html', {'data': data})