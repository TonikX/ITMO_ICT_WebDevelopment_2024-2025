from django.db.models import Exists, OuterRef, Q

from .forms import UserRegistrationForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from .models import Ticket, Races, Places, Bookings


def logout_view(request):
    logout(request)
    return redirect('/')

def login_view(request):
    if request.method == "POST":
        user_form = LoginForm(request.POST)
        if user_form.is_valid():
            cleaned_data = user_form.cleaned_data
            user = authenticate(username=cleaned_data['username'], password=cleaned_data['password'])
            if user is None:
                return render(request, 'login.html')
            login(request, user)
            return redirect("/")
    else:
        user_form = LoginForm()
    return render(request, 'login.html', {'user_form': user_form})

def profile(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html')
    return render(request, 'home.html')

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect("/")
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})

def my_races(request):
    if not request.user.is_authenticated:
        return redirect("/")
    tickets = Ticket.objects.filter(user=request.user.id, race__is_departure=True)
    return render(request, "my_races.html", {"tickets": tickets})

def race(request, race_id):
    race_data = Races.objects.filter(pk=race_id).first()
    if race_data is None:
        return redirect("/")

    ticket_data = Ticket.objects.filter(race=race_data.id, user=request.user.id).first()
    booking_data = Bookings.objects.filter(ticket=ticket_data).first()

    if request.method == "POST":
        if ticket_data is None:
            return redirect(f"/race/{race_id}")

        place = Places.objects.filter(pk=request.POST["place"]).first()
        if place is None:
            return redirect(f"/race/{race_id}")

        if booking_data is None:
            booking_data = Bookings()
            booking_data.ticket = ticket_data

        booking_data.place = place
        booking_data.save()

        return redirect(f"/race/{race_id}")
    if not request.user.is_authenticated:
        return redirect("/")

    places_data = Places.objects.annotate(
        booked=Exists(Bookings.objects.filter(~Q(ticket__user=request.user.id), place=OuterRef('pk')))
    ).values('row', 'col', 'id', 'booked').order_by('booked', 'row', 'col').all()

    all_bookings_data = Bookings.objects.filter(ticket__race=ticket_data.race).order_by('place__row', 'place__col').all()

    return render(request, "race.html", {"race": race_data, "ticket": ticket_data, "booking": booking_data, "places": places_data, "all_bookings": all_bookings_data})