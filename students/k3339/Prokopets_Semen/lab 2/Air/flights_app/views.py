from flights_app.forms import *
from flights_app.models import User, Flight, Ticket, Feedback
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import BookForm
import time

def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return render(request, 'auth.html')


def logout_view(request):
    logout(request)
    return redirect('/')


def auth(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'auth.html', {'error': 'Try again'})


def registration(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = NewUserForm()
    return render(request, "register.html", {"register_form": form})


def tickets(request):
    user_tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'tickets.html', {'tickets': user_tickets})


def flights(request):
    return render(request, 'flights.html', {'flights': Flight.objects.all()})


def users_list(request, flight_id):
    user_ids = Ticket.objects.filter(flight_id=flight_id).values('user_id')
    users = User.objects.filter(id__in=user_ids)
    flight = Flight.objects.get(id=flight_id)
    return render(request, "users.html", {
        "users": users,
        "flight": flight,
    })


def feedbacks(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    feedbacks = Feedback.objects.filter(flight_id=flight_id)
    return render(request, "feedbacks.html", {
        "feedbacks": feedbacks,
        "flight": flight,
    })


def create_feedback(request, flight_id):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            Feedback.objects.create(comment=form.cleaned_data.get('comment'),
                                    rate=form.cleaned_data.get('rating'),
                                    date=form.cleaned_data.get('date'),
                                    user_id=request.user.id,
                                    flight_id=flight_id)

            return redirect('/flights')
    else:
        form = FeedbackForm()
    return render(request, 'leave_feedback.html', {'form': form})


def delete_ticket(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    if ticket.user_id == request.user.id:
        ticket.delete()
    return redirect('/tickets')


@login_required
def update_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)

    if ticket.user_id != request.user.id:
        return redirect('/')

    if request.method == 'POST':
        form = TicketUpdateForm(request.POST)
        if form.is_valid():
            ticket.seat = form.cleaned_data.get('seat')
            ticket.save()
            return redirect('/tickets')
    else:
        form = TicketUpdateForm(initial={'seat': ticket.seat})

    return render(request, 'update.html', {'form': form, 'ticket': ticket})


@login_required
def book_flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            seat = form.cleaned_data.get('seat')
            if Ticket.objects.filter(flight=flight, seat=seat).exists():
                form.add_error('seat', "Это место уже забронировано.")
            else:
                ticket_id = int(str(time.time_ns())[-7:])
                Ticket.objects.create(
                    ticket_id=ticket_id,
                    seat=seat,
                    flight=flight,
                    user=request.user,
                    type=form.cleaned_data.get('type'),
                )
                return redirect('/tickets')
    else:
        form = BookForm()

    return render(request, 'book.html', {'form': form, 'flight': flight})
@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_bookings(request):
    tickets = Ticket.objects.all()

    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        action = request.POST.get('action')

        ticket = get_object_or_404(Ticket, ticket_id=ticket_id)

        if action == 'confirm':
            ticket.is_confirmed = True
            ticket.save()
        elif action == 'reject':
            ticket.delete()

        return redirect('/tickets')

    return render(request, 'manage_bookings.html', {'tickets': tickets})