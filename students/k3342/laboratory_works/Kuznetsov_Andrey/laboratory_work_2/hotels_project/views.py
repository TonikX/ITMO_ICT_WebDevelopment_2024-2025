from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import Hotel, Room, Reservation
from .forms import ReservationForm, ReviewForm, SignUpForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def profile(request):
    return render(request, "profile.html", {"user": request.user})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("hotel_list")
            else:
                messages.error(request, "Неверные данные для входа.")
        else:
            messages.error(request, "Неверные данные для входа.")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("hotel_list")


class HotelListView(ListView):
    model = Hotel
    template_name = "hotel_list.html"
    context_object_name = "hotels"


class HotelDetailView(DetailView):
    model = Hotel
    template_name = "hotel_detail.html"
    context_object_name = "hotel"


@login_required
def reserve_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.client = request.user
            reservation.room = room
            reservation.save()
            return redirect("reservation_list")
    else:
        form = ReservationForm()
    return render(request, "reserve_room.html", {"form": form, "room": room})


@login_required
def reservation_list(request):
    reservations = Reservation.objects.filter(client=request.user)
    return render(request, "reservation_list.html", {"reservations": reservations})


@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, client=request.user)
    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect("reservation_list")
    else:
        form = ReservationForm(instance=reservation)
    return render(request, "edit_reservation.html", {"form": form, "reservation": reservation})


@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, client=request.user)
    if request.method == "POST":
        reservation.delete()
        return redirect("reservation_list")
    return render(request, "delete_reservation.html", {"reservation": reservation})


@login_required
def add_review(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.room = room
            review.save()
            return redirect("hotel_detail", pk=room.hotel.id)
    else:
        form = ReviewForm()
    return render(request, "add_review.html", {"form": form, "room": room})


@login_required
def recent_guests(request):
    reservations = Reservation.get_last_month_reservations()
    return render(request, "recent_guests.html", {"reservations": reservations})
