from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Q
from .models import Tour, Reservation, Review
from django.contrib.auth import login, logout
from .forms import UserRegistrationForm, ReservationForm, ReviewForm, SearchForm
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    tour_list = Tour.objects.all().order_by('-created_at')
    
    # Обработка поиска
    form = SearchForm(request.GET or None)
    search_query = request.GET.get('query', '')
    selected_country = request.GET.get('country', '')
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        country = form.cleaned_data.get('country')
        
        if query:
            tour_list = tour_list.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(country__icontains=query) |
                Q(agency__icontains=query)
            )
        
        if country:
            tour_list = tour_list.filter(country=country)

    # Пагинация
    paginator = Paginator(tour_list, 6)
    page = request.GET.get('page')
    
    try:
        tours = paginator.page(page)
    except PageNotAnInteger:
        tours = paginator.page(1)
    except EmptyPage:
        tours = paginator.page(paginator.num_pages)
    
    return render(request, 'home.html', {
        'tours': tours,
        'form': form,
        'search_query': search_query,
        'selected_country': selected_country
    })

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

@csrf_protect
def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Вы успешно вышли из системы.')
        return redirect('login')
    else:
        # Если кто-то попытается выйти через GET, перенаправляем на главную
        return redirect('home')

@login_required
def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    user_reservation = None
    user_review = None
    
    if request.user.is_authenticated:
        user_reservation = Reservation.objects.filter(user=request.user, tour=tour).first()
        user_review = Review.objects.filter(user=request.user, tour=tour).first()
    
    reviews = Review.objects.filter(tour=tour).exclude(user=request.user)
    
    if request.method == 'POST':
        if 'reserve' in request.POST:
            reservation_form = ReservationForm(request.POST)
            if reservation_form.is_valid() and not user_reservation:
                reservation = reservation_form.save(commit=False)
                reservation.user = request.user
                reservation.tour = tour
                reservation.save()
                messages.success(request, 'Тур успешно забронирован!')
                return redirect('tour_detail', tour_id=tour_id)
        
        elif 'review' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                if user_review:
                    review_form = ReviewForm(request.POST, instance=user_review)
                    review = review_form.save()
                    messages.success(request, 'Отзыв обновлен!')
                else:
                    review = review_form.save(commit=False)
                    review.user = request.user
                    review.tour = tour
                    review.save()
                    messages.success(request, 'Отзыв добавлен!')
                return redirect('tour_detail', tour_id=tour_id)
    else:
        reservation_form = ReservationForm(instance=user_reservation)
        review_form = ReviewForm(instance=user_review)
    
    return render(request, 'tour_detail.html', {
        'tour': tour,
        'reservation_form': reservation_form,
        'review_form': review_form,
        'user_reservation': user_reservation,
        'user_review': user_review,
        'reviews': reviews,
    })

@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'my_reservations.html', {'reservations': reservations})

@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Резервирование обновлено!')
            return redirect('my_reservations')
    else:
        form = ReservationForm(instance=reservation)
    
    return render(request, 'edit_reservation.html', {'form': form, 'reservation': reservation})

@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, 'Резервирование удалено!')
        return redirect('my_reservations')
    
    return render(request, 'delete_reservation.html', {'reservation': reservation})

def sold_tours_by_country(request):
    # Туры с подтвержденными резервированиями
    sold_tours = Tour.objects.filter(
        reservation__status='confirmed'
    ).annotate(
        reservations_count=Count('reservation'),
        total_sold=Sum('reservation__tour__price')
    ).order_by('country')
    
    return render(request, 'sold_tours.html', {'sold_tours': sold_tours})