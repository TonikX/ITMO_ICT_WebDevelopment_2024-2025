from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from .models import Tour, Basket, Booking
from django.views.decorators.csrf import csrf_protect
from .forms import TourForm, ReviewForm
from django.core.paginator import Paginator

# Create your views here.

def Index(request, page=1):
    tours = Tour.objects.all()
    paginator = Paginator(tours, 3)
    tours_paginator = paginator.page(page)
    context = {
        'tours': tours_paginator
    }
    return render(request, 'tour/index.html', context)

@csrf_protect
def addTour(request):
    if request.method == "POST":
        form = TourForm(request.POST)
        if form.is_valid():
            tour = form.save(commit=False)  # Используем переменную 'tour', чтобы избежать конфликта с моделью
            tour.save()  # Сохраняем объект в базе данных
            return HttpResponseRedirect(reverse('Index'))
        else:
            print("Ошибки формы:", form.errors)
    else:
        form = TourForm()

    context = {'form': form}
    return render(request, 'tour/addTour.html', context)

def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    reviews = tour.reviews.all()  # Получаем все отзывы для данного тура

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.tour = tour  # Привязываем отзыв к конкретному туру
            review.user = request.user  # Привязываем отзыв к текущему пользователю
            review.save()
            return HttpResponseRedirect(reverse('tour_detail', args=[tour.id]))
    else:
        form = ReviewForm()

    context = {
        'tour': tour,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'tour/abouttour.html', context)

def basket_add(request, tour_id):
    tour = Tour.objects.get(id=tour_id)
    baskets = Basket.objects.filter(user=request.user, tour=tour)

    if not baskets.exists():
        Basket.objects.create(user=request.user, tour=tour, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def basket_view(request):
    baskets = Basket.objects.filter(user=request.user)
    total_price = sum(basket.tour.price * basket.quantity for basket in baskets)

    context = {
        'baskets': baskets,
        'total_price': total_price,
    }
    return render(request, 'tour/basket.html', context)


def confirm_booking(request):
    baskets = Basket.objects.filter(user=request.user)

    for basket in baskets:
        # Создаем бронирование для каждого элемента корзины
        Booking.objects.create(
            user=request.user,
            tour=basket.tour,
            quantity=basket.quantity
        )
        basket.delete()  # Удаляем элемент из корзины после переноса

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def booking_views(request):
    bookings = Booking.objects.all()
    baskets = Basket.objects.filter(user=request.user)
    total_price = sum(basket.tour.price * basket.quantity for basket in baskets)

    context = {
        'bookings': bookings
    }
    return render(request, 'tour/bookings.html', context)
