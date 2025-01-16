from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from .forms import ReviewForm
from .models import Flight, Ticket, FlightReview, TicketReservation


class FlightsList(LoginRequiredMixin, ListView):
    model = Flight
    template_name = 'flights/list.html'
    context_object_name = 'flights'
    paginate_by = 10
    login_url = '/accounts/login/'


@login_required(login_url='/accounts/login/')
def flight_details(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    tickets = Ticket.objects.filter(flight=flight)
    reservations = TicketReservation.objects.filter(flight=flight, ticket__isnull=True)
    reviews = FlightReview.objects.filter(flight=flight)
    user_reservation = reservations.filter(passenger=request.user).first()
    has_reviewed = reviews.filter(author=request.user).exists()

    context = {
        'flight': flight,
        'tickets': tickets,
        'reservations': reservations if request.user.is_staff else None,
        'user_reservation': user_reservation,
        'reviews': reviews,
        'has_reviewed': has_reviewed,
        'is_admin': request.user.is_staff,
    }
    return render(request, 'flights/detail.html', context)


@login_required(login_url='/accounts/login/')
def add_review(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.flight = flight
            review.author = request.user
            review.save()
            return redirect('flight_details', flight_id=flight.id)
    else:
        form = ReviewForm()

    return render(request, 'reviews/add.html', {'flight': flight, 'form': form})


@login_required(login_url='/accounts/login/')
def delete_ticket_reservation(request, reservation_id):
    reservation = get_object_or_404(TicketReservation, id=reservation_id)

    if reservation.passenger != request.user:
        return HttpResponseForbidden("You are not authorized to delete this reservation.")

    if request.method == "POST":
        reservation.delete()
        messages.success(request, "Ticket reservation deleted successfully.")
        return redirect('flight_details', flight_id=reservation.flight.id)

    return render(request, 'tickets/delete_reservation.html', {'reservation': reservation})


@login_required(login_url='/accounts/login/')
def reserve_ticket(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == 'POST':
        if not TicketReservation.objects.filter(flight=flight, passenger=request.user).exists():
            TicketReservation.objects.create(flight=flight, passenger=request.user)
            return redirect('flight_details', flight_id=flight.id)
        else:
            error_message = "You have already reserved a ticket for this flight."
            return render(request, 'tickets/reserve.html', {'flight': flight, 'error_message': error_message})

    return render(request, 'tickets/reserve.html', {'flight': flight})


@staff_member_required
def confirm_reservation(request, reservation_id):
    reservation = get_object_or_404(TicketReservation, id=reservation_id)

    if request.method == 'POST':
        seat_number = request.POST.get('seat_number')

        if Ticket.objects.filter(flight=reservation.flight, seat_number=seat_number).exists():
            return render(request, 'tickets/confirm_reservation.html', {
                'reservation': reservation,
                'error_message': "This seat number is already taken.",
            })

        Ticket.objects.create(
            flight=reservation.flight,
            passenger=reservation.passenger,
            seat_number=seat_number,
            reservation=reservation
        )

        return redirect('flight_details', flight_id=reservation.flight.id)

    return render(request, 'tickets/confirm_reservation.html', {
        'reservation': reservation,
    })


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.user == ticket.passenger or request.user.is_staff:
        ticket.delete()
        messages.success(request, "Ticket deleted successfully.")
    else:
        messages.error(request, "You do not have permission to delete this ticket.")

    return redirect('flight_details', flight_id=ticket.flight.id)
