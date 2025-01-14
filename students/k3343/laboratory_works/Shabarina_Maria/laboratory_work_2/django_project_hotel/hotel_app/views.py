from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, ReviewForm
from .models import Hotel, Room, Reservation, Review
from django.core.paginator import Paginator


def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.user_type == 'admin' and form.cleaned_data['managed_hotel']:
                user.managed_hotel = form.cleaned_data['managed_hotel']
                user.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('all_hotels')


def get_all_hotels(request):
    query = request.GET.get('query', '')
    if query:
        hotels = Hotel.objects.filter(name__icontains=query)
    else:
        hotels = Hotel.objects.all()
    paginator = Paginator(hotels, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'hotels.html', {'page_obj': page_obj, 'query': query,})


def get_hotel_info(request, hotel_id):
    try:
        hotel = Hotel.objects.get(pk=hotel_id)
    except:
        raise Http404("Hotel does not exist")
    rooms = hotel.rooms.all()
    return render(request, 'hotel_info.html', {'hotel': hotel, 'rooms': rooms})


@login_required
def user_get_all_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'user_reservations.html', {'reservations': reservations})


@login_required
def admin_get_all_reservations(request):
    hotel = request.user.managed_hotel
    reservations = Reservation.objects.filter(hotel=hotel)
    return render(request, 'admin_reservations.html', {'reservations': reservations, 'hotel': hotel})


@login_required
def create_reservation(request, room_id):
    try:
        room = Room.objects.get(pk=room_id)
    except Room.DoesNotExist:
        raise Http404("Room does not exist")
    user = request.user
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reservation = Reservation(user=user, hotel=room.hotel, room=room, start_date=start_date, end_date=end_date)
        reservation.save()
        return redirect('user_reservations')
    return render(request, 'create_reservation.html', {'room': room})


@login_required
def update_reservation(request, reservation_id):
    try:
        reservation = Reservation.objects.get(pk=reservation_id)
    except Reservation.DoesNotExist:
        raise Http404("Reservation does not exist")
    if request.method == 'POST':
        reservation.start_date = request.POST.get('start_date')
        reservation.end_date = request.POST.get('end_date')
        reservation.save()
        return redirect('all_reservations')
    return render(request, 'update_reservation.html', {'reservation': reservation})


@login_required
def delete_reservation(request, reservation_id):
    try:
        reservation = Reservation.objects.get(pk=reservation_id)
    except Reservation.DoesNotExist:
        raise Http404("Reservation does not exist")
    if request.method == 'POST':
        reservation.delete()
        return redirect('user_reservations')
    return render(request, 'delete_reservation.html', {'reservation': reservation})


@login_required
def create_review(request, reservation_id):
    try:
        reservation = Reservation.objects.get(pk=reservation_id, user=request.user)
    except Reservation.DoesNotExist:
        raise Http404("Reservation does not exist")
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reservation = reservation
            review.user = request.user
            review.save()
            return redirect('user_reservations')
    else:
        form = ReviewForm()
    return render(request, 'create_review.html', {'form': form, 'reservation': reservation})


@login_required
def get_all_reviews(request, room_id):
    try:
        room = Room.objects.get(pk=room_id)
    except Room.DoesNotExist:
        raise Http404("Room does not exist")
    reviews = Review.objects.filter(reservation__room=room)
    return render(request, 'all_reviews.html', {'room': room, 'reviews': reviews})


@login_required
def confirm_reservation(request, reservation_id):
    try:
        reservation = Reservation.objects.get(pk=reservation_id)
    except:
        raise Http404("Reservation does not exist")
    if reservation.hotel == request.user.managed_hotel:
        reservation.status = 'checked_in'
        reservation.save()
        return redirect('admin_reservations')
    return redirect('all_hotels')


@login_required
def decline_reservation(request, reservation_id):
    try:
        reservation = Reservation.objects.get(pk=reservation_id)
    except:
        raise Http404("Reservation does not exist")
    if reservation.hotel == request.user.managed_hotel:
        reservation.status = 'checked_out'
        reservation.save()
        return redirect('admin_reservations')
    return redirect('all_hotels')
