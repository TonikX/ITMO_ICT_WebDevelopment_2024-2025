from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Hotel, HotelForm, Room, Reservation, Review, RoomForm
from django.contrib.auth.decorators import login_required
import datetime


def home_view(request):
    reservations = Reservation.objects.filter(user=request.user.id)
    return render(request, "base.html", {"reservations": reservations})


def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, "hotel_list.html", {"hotels": hotels})


@login_required(login_url="login")
def add_review(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == "POST":
        comment = request.POST["comment"]
        rating = request.POST["rating"]
        review = Review(
            user=request.user,
            room=room,
            comment=comment,
            rating=rating,
        )
        print(review)
        review.save()

        return redirect("hotel_list")
    return render(request, "add_review.html", {"room": room})


@login_required(login_url="login")
def create_hotel(request):
    if request.method == "POST":
        form = HotelForm(request.POST)
        if form.is_valid():
            hotel = form.save()
            return redirect("view_hotel", pk=hotel.pk)
    else:
        form = HotelForm()
    return render(request, "create_hotel.html", {"form": form})


@login_required(login_url="login")
def view_hotel(request, pk):
    hotel = Hotel.objects.get(pk=pk)
    rooms = Room.objects.filter(hotel=hotel)
    reviews = Review.objects.all()
    now = datetime.datetime.now()
    last_month_start = now.replace(day=1) - datetime.timedelta(days=1)
    last_month_end = last_month_start.replace(day=1)

    # Filter reservations for the last month
    reservations = Reservation.objects.all()
    return render(
        request,
        "view_hotel.html",
        {
            "hotel": hotel,
            "rooms": rooms,
            "reviews": reviews,
            "reservations": reservations,
        },
    )


@login_required(login_url="login")
def create_room(request, hotel_pk):
    hotel = Hotel.objects.get(pk=hotel_pk)
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.hotel = hotel
            room.save()
            return redirect("view_hotel", pk=hotel.pk)
    else:
        form = RoomForm()
    return render(request, "create_room.html", {"form": form, "hotel": hotel})


@login_required(login_url="login")
def book_room(request, hotel_pk):
    if request.method == "POST":
        # Retrieve the selected room and reservation details from the form data
        room_id = request.POST["room_id"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        hotel = Hotel.objects.get(pk=hotel_pk)

        # Create a new Reservation object
        reservation = Reservation(
            hotel=hotel,
            user=request.user,
            room_id=room_id,
            start_date=start_date,
            end_date=end_date,
        )
        reservation.save()

        # Update the availability of the room
        room = Room.objects.get(id=room_id)
        room.available = False
        room.save()

        return redirect("reservation_success")

    else:
        # Retrieve the selected hotel and rooms from the database
        hotel = Hotel.objects.get(pk=hotel_pk)
        rooms = Room.objects.filter(hotel=hotel)

        # Pass the hotel and rooms as context to the template
        return render(
            request, "room_reservation.html", {"hotel": hotel, "rooms": rooms}
        )


def reservation_success(request):
    return render(request, "reservation_success.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            print(form)
            return redirect("login")
        print(form)
    else:
        form = UserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")  # replace 'home' with your desired URL after login
        else:
            return redirect("login")  # or display an error message
    return render(request, "accounts/login.html")


@login_required(login_url="login")
def logout_view(request):
    logout(request)
    return redirect("login")


def room_reviews(request, room_id):
    room = Room.objects.get(id=room_id)
    reviews = Review.objects.filter(room=room)
    return render(
        request,
        "room_reviews.html",
        {"room": room, "reviews": reviews},
    )
