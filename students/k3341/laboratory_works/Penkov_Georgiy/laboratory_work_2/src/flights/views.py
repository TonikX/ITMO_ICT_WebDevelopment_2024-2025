from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.http import HttpResponseForbidden
from flights.models import Flight, PassengerRegistration, Feedback
from flights.forms import ReserveSeatForm, FeedbackForm


class FlightListView(ListView):
    model = Flight
    context_object_name = "flights"
    paginate_by = 5

    def get_queryset(self):
        flights = Flight.objects.order_by("-datetime")
        query = self.request.GET.get("q")
        if query:
            flights = flights.filter(
                Q(number__icontains=query)
                | Q(direction__icontains=query)
                | Q(airline__name__icontains=query)
            )

        return flights

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q")
        return context


def flight_detail_view(request, pk):
    flight = get_object_or_404(Flight, pk=pk)
    registrations = PassengerRegistration.objects.filter(flight=flight)
    reserve_seat_form = ReserveSeatForm()

    if request.user.is_authenticated:
        try:
            passenger_registration = PassengerRegistration.objects.get(
                flight=flight, passenger=request.user
            )
            user_registration_status = passenger_registration.status
        except PassengerRegistration.DoesNotExist:
            user_registration_status = None
    else:
        user_registration_status = None

    feedbacks = Feedback.objects.filter(flight=flight).order_by("-created_at")
    feedback_form = FeedbackForm()

    return render(
        request,
        "flights/flight_detail.html",
        {
            "flight": flight,
            "reserve_seat_form": reserve_seat_form,
            "user_registration_status": user_registration_status,
            "registrations": registrations,
            "feedbacks": feedbacks,
            "feedback_form": feedback_form,
        },
    )


def reserve_seat(request, flight_id):
    if not request.method == "POST":
        return HttpResponseForbidden("Invalid request method.")
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to reserve a seat.")

    form = ReserveSeatForm(request.POST)

    if form.is_valid():
        flight = get_object_or_404(Flight, pk=flight_id)
        seat = form.cleaned_data["seat"]

        if PassengerRegistration.objects.filter(flight=flight, seat=seat).exists():
            return HttpResponseForbidden("This seat is already taken.")

        if PassengerRegistration.objects.filter(
            flight=flight, passenger=request.user
        ).exists():
            return HttpResponseForbidden("You can't have more than one registration")

        passenger_registration = form.save(commit=False)
        passenger_registration.flight = flight
        passenger_registration.passenger = request.user
        passenger_registration.status = "RESERVED"
        passenger_registration.save()

    return redirect("flights:flight-detail", pk=flight_id)


def my_registrations(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to see your registrations.")
    registrations = PassengerRegistration.objects.filter(passenger=request.user)

    return render(
        request, "flights/my_registrations.html", {"registrations": registrations}
    )


def delete_registration(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    user = request.user

    if not user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to cancel registration.")
    registration = get_object_or_404(
        PassengerRegistration, flight=flight, passenger=user
    )
    registration.delete()

    return redirect("flights:my-registrations")


def leave_feedback(request, flight_id):
    if not request.method == "POST":
        return HttpResponseForbidden("Invalid request method.")
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to leave a feedback.")
    form = FeedbackForm(request.POST)
    if form.is_valid():
        feedback = form.save(commit=False)
        feedback.flight = get_object_or_404(Flight, pk=flight_id)
        feedback.author = request.user
        feedback.save()
    return redirect("flights:flight-detail", pk=flight_id)
