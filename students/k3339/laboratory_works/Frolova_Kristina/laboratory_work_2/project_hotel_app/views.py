from datetime import timedelta, datetime

from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_request
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.views.generic import ListView, DeleteView, UpdateView

from project_hotel_app.forms import ReservationCreateForm, ReviewCreateForm
from project_hotel_app.models import Room, Reservation, Hotel, Review


@login_required(login_url='/login/')
def user_reservations(request):
    reservations = Reservation.objects.filter(user_id=request.user)
    return render(request, "reservation/reservations.html", {"reservations": reservations})


def month_clients(request):
    last_month = datetime.now() - timedelta(days=30)
    reservations = Reservation.objects.filter(start_date__gt=last_month)
    return render(request, "hotel/month_clients.html", {"reservations_of_this_month": reservations})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print(form)
            form.save()
            return redirect("/login/")
    else:
        form = UserCreationForm()
    return render(request, "account/register.html", {"form": form})


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login_request(request, user)
            return redirect("/reservations/")
        else:
            return redirect("/login/")
    return render(request, "account/login.html")


def hotel_rooms(request, hotel_id):
    rooms = Room.objects.filter(hotel_id=hotel_id)
    return render(request, "hotel/rooms.html", {"rooms": rooms})


@login_required(login_url='/login/')
def create_reservation(request, room_id):
    room = Room.objects.get(id=room_id)
    user = request.user
    context = {}
    form = ReservationCreateForm(
        request.POST or None)
    if form.is_valid():
        reservation = form.save(commit=False)
        reservation.user = user
        reservation.room = room
        form.save()
        return redirect("/reservations/")
    context['form'] = form
    return render(request, "reservation/reservation_create.html", context)

def room_reviews(request, room_id):
    room = Room.objects.get(id=room_id)
    try:
        reservation = Reservation.objects.get(room=room)
        reviews = Review.objects.filter(reservation=reservation)
    except Reservation.DoesNotExist:
        reviews = []
    return render(
        request,
        "hotel/room_reviews.html",
        {"room": room, "reviews": reviews},
    )


@login_required(login_url="/login/")
def create_review(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    context = {}
    form = ReviewCreateForm(
        request.POST or None)
    if form.is_valid():
        review = form.save(commit=False)
        review.reservation = reservation
        form.save()
        return redirect(f"/rooms/{reservation.room.id}/reviews/")
    context['form'] = form
    return render(request, "hotel/review_create.html", context)


class HotelListView(ListView):
    model = Hotel
    context_object_name = 'hotels'
    template_name = "hotel/hotels.html"


class ReservationDeleteView(DeleteView):
    model = Reservation
    success_url = "/reservations/"
    template_name = 'reservation/reservation_delete.html'


class ReservationUpdateView(UpdateView):
    model = Reservation
    fields = ['start_date', 'end_date']
    success_url = '/reservations/'
    template_name = 'reservation/reservation_update.html'
