from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Tour, Reservation, Review
from .forms import ReservationForm, ReviewForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.contrib.auth import logout

def tour_list(request):
    tours = Tour.objects.all()
    return render(request, 'tours/tour_list.html', {'tours': tours})

def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    reviews = Review.objects.filter(tour=tour)

    is_reserved = False
    if request.user.is_authenticated:
        is_reserved = Reservation.objects.filter(user=request.user, tour=tour).exists()

    return render(request, 'tours/tour_detail.html', {
        'tour': tour,
        'reviews': reviews,
        'is_reserved': is_reserved
    })
def custom_logout(request):
    logout(request)
    return redirect('tour_list')
@login_required
def cancel_reservation(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    reservation = Reservation.objects.filter(user=request.user, tour=tour).first()
    if reservation:
        reservation.delete()

    return redirect('tour_detail', tour_id=tour.id)
@login_required
def reserve_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if Reservation.objects.filter(user=request.user, tour=tour).exists():
        return redirect('tour_detail', tour_id=tour.id)
    Reservation.objects.create(user=request.user, tour=tour)
    return redirect('tour_detail', tour_id=tour.id)

@login_required
def add_review(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.tour = tour
            review.save()
            return redirect('tour_detail', tour_id=tour.id)
    else:
        form = ReviewForm()
    return render(request, 'tours/add_review.html', {'form': form, 'tour': tour})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Вход после регистрации
            return redirect('tour_list')  # Замените 'home' на вашу главную страницу
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('tour_list')  # Замените 'home' на вашу главную страницу
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

