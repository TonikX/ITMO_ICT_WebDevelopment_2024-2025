from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import Hotel, Room, Reservation
from .forms import ReservationForm, ReviewForm


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
            reservation.user = request.user
            reservation.room = room
            reservation.save()
            return redirect("reservation_list")
    else:
        form = ReservationForm()
    return render(request, "hotels/reserve_room.html", {"form": form, "room": room})


@login_required
def reservation_list(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, "hotels/reservation_list.html", {"reservations": reservations})


@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
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
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == "POST":
        reservation.delete()
        return redirect("reservation_list")
    return render(request, "hotels/delete_reservation.html", {"reservation": reservation})


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
    from django.utils.timezone import now, timedelta

    last_month = now() - timedelta(days=30)
    reservations = Reservation.objects.filter(
        check_in__gte=last_month, check_out__lte=now()
    )
    return render(request, "recent_guests.html", {"reservations": reservations})
