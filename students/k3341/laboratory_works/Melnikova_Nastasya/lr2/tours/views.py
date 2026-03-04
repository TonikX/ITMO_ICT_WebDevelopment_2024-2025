from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Tour, Reservation, Review  # ← добавили Review сюда
from django.db.models import Count

# ===== Главная страница: список туров =====
def tour_list(request):
    tours = Tour.objects.all()
    return render(request, 'tours/tour_list.html', {'tours': tours})


# ===== Регистрация пользователя =====
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'tours/register.html', {'form': form})


# ===== Бронирование тура =====
@login_required
def reserve_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    Reservation.objects.create(user=request.user, tour=tour)
    return redirect('my_reservations')


# ===== Просмотр своих броней =====
@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'tours/my_reservations.html', {'reservations': reservations})


# ===== Удаление брони =====
@login_required
def delete_reservation(request, res_id):
    res = get_object_or_404(Reservation, id=res_id, user=request.user)
    res.delete()
    return redirect('my_reservations')


# ===== Добавление отзыва =====
@login_required
def add_review(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        comment = request.POST['comment']
        rating = int(request.POST['rating'])
        Review.objects.create(
            user=request.user,
            tour=tour,
            comment=comment,
            rating=rating
        )
        return redirect('tour_detail', tour_id=tour.id)
    return render(request, 'tours/add_review.html', {'tour': tour})


# ===== Просмотр отдельного тура + отзывы =====
def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    reviews = Review.objects.filter(tour=tour)
    return render(request, 'tours/tour_detail.html', {
        'tour': tour,
        'reviews': reviews
    })

def sold_tours(request):
    data = (
        Reservation.objects.filter(confirmed=True)
        .values('tour__country', 'tour__name', 'tour__agency')
        .annotate(sold_count=Count('id'))
        .order_by('tour__country', '-sold_count')
    )
    return render(request, 'tours/sold_tours.html', {'data': data})


