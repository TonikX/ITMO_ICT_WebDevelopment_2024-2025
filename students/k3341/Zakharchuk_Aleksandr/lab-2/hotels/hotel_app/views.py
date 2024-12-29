import datetime

from django import http
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_request
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic

from hotel_app import forms, models


def root(request: http.HttpRequest) -> http.HttpResponse:
    return redirect(reverse("hotels"))


def register(request: http.HttpRequest) -> http.HttpResponse:
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("login"))
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})


def login(request: http.HttpRequest) -> http.HttpResponse:
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)

        if user is not None:
            login_request(request, user)
            return redirect("/reservations/")

        return redirect(reverse("login"))

    return render(request, "login.html")


@login_required(login_url="/login/")
def user_reservations(request: http.HttpRequest) -> http.HttpResponse:
    reservations = models.Reservation.objects.filter(user_id=request.user)
    return render(request, "reservations.html", {"reservations": reservations})


def hotel_rooms(request: http.HttpRequest, hotel_id: int) -> http.HttpResponse:
    rooms = models.Room.objects.filter(hotel_id=hotel_id)
    return render(request, "rooms.html", {"rooms": rooms})


@login_required(login_url="/login/")
def create_reservation(request: http.HttpRequest, room_id: int) -> http.HttpResponse:
    form = forms.CreateReservationForm(request.POST or None)
    room = models.Room.objects.get(id=room_id)

    if form.is_valid():
        reservation = form.save(commit=False)
        reservation.user = request.user
        reservation.room = room
        form.save()
        return redirect(reverse("reservations"))

    return render(request, "create_reservation.html", {"form": form, "room": room})


@login_required(login_url="/login/")
def create_review(request: http.HttpRequest, reservation_id: int) -> http.HttpResponse:
    reservation = models.Reservation.objects.get(id=reservation_id)
    form = forms.CreateReviewForm(request.POST or None)

    if form.is_valid():
        review = form.save(commit=False)
        review.reservation = reservation
        form.save()
        return redirect(f"/rooms/{reservation.room.id}/reviews/")

    return render(request, "create_review.html", {"form": form, "reservation": reservation})


def room_reviews(request: http.HttpRequest, room_id: int) -> http.HttpResponse:
    room = models.Room.objects.get(id=room_id)
    all_reviews = []

    try:
        reservations = models.Reservation.objects.filter(room=room)
        for reservation in reservations:
            reviews = models.Review.objects.filter(reservation=reservation)
            all_reviews.extend(reviews)

    except models.Reservation.DoesNotExist as err:
        print(err)

    return render( request, "room_reviews.html", {"room": room, "reviews": all_reviews})


@user_passes_test(lambda user: user.is_staff, login_url="/login/")
def month_clients(request: http.HttpRequest) -> http.HttpResponse:
    last_month = datetime.datetime.now() - datetime.timedelta(days=30)
    reservations = models.Reservation.objects.order_by("start_date").filter(start_date__gt=last_month)
    return render(request, "month_clients.html", {"reservations": reservations})


class HotelListView(generic.ListView):
    model = models.Hotel
    context_object_name = "hotels"
    template_name = "hotels.html"


class UpdateReservationView(generic.UpdateView):
    model = models.Reservation
    form_class = forms.UpdateReservationForm
    success_url = "/reservations/"
    template_name = "update_reservation.html"


class DeleteReservationView(generic.DeleteView):
    model = models.Reservation
    success_url = "/reservations/"
    template_name = "delete_reservation.html"
