from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import (
    Avg,
    Count,
    DecimalField,
    ExpressionWrapper,
    F,
    Q,
    Sum,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import BookingForm, ReviewForm, SignUpForm
from .models import Booking, Country, Review, Tour


def tour_list(request):
    tours = (
        Tour.objects
        .filter(is_active=True)
        .select_related("country", "agency")
    )

    query = request.GET.get("q", "").strip()
    country_id = request.GET.get("country", "").strip()

    if query:
        tours = tours.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(country__name__icontains=query)
        )

    if country_id:
        if (
            country_id.isascii()
            and country_id.isdigit()
            and len(country_id) <= 18
        ):
            tours = tours.filter(country_id=country_id)
        else:
            country_id = ""

    paginator = Paginator(tours, 6)
    page = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "tours/tour_list.html",
        {
            "page": page,
            "countries": Country.objects.all(),
            "query": query,
            "selected_country": country_id,
        },
    )


def tour_detail(request, pk):
    tour = get_object_or_404(
        Tour.objects.select_related("country", "agency"),
        pk=pk,
    )

    reviews = tour.reviews.select_related("user").all()
    average_rating = reviews.aggregate(value=Avg("rating"))["value"]
    today = timezone.localdate()
    booking_closed_reason = None

    if not tour.is_active:
        booking_closed_reason = "Booking unavailable"
    elif tour.end_date < today:
        booking_closed_reason = "Tour completed"
    elif tour.start_date <= today:
        booking_closed_reason = "Booking closed"
    elif tour.available_seats == 0:
        booking_closed_reason = "Sold out"

    can_review = False

    if request.user.is_authenticated:
        can_review = (
            Booking.objects.filter(
                user=request.user,
                tour=tour,
                status=Booking.Status.CONFIRMED,
            ).exists()
            and not Review.objects.filter(
                user=request.user,
                tour=tour,
            ).exists()
            and tour.end_date < today
        )

    return render(
        request,
        "tours/tour_detail.html",
        {
            "tour": tour,
            "reviews": reviews,
            "average_rating": average_rating,
            "can_review": can_review,
            "booking_closed_reason": booking_closed_reason,
        },
    )


def register(request):
    if request.user.is_authenticated:
        return redirect("tour_list")

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                "Registration completed successfully.",
            )

            return redirect("tour_list")
    else:
        form = SignUpForm()

    return render(
        request,
        "registration/register.html",
        {"form": form},
    )


@login_required
def create_booking(request, pk):
    tour = get_object_or_404(
        Tour,
        pk=pk,
        is_active=True,
    )

    if tour.start_date <= timezone.localdate():
        messages.error(
            request,
            "This tour can no longer be booked.",
        )
        return redirect("tour_detail", pk=tour.pk)

    if tour.available_seats == 0:
        messages.error(
            request,
            "There are no available seats.",
        )
        return redirect("tour_detail", pk=tour.pk)

    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():
            persons = form.cleaned_data["persons"]

            if persons > tour.available_seats:
                form.add_error(
                    "persons",
                    f"Only {tour.available_seats} seats are available.",
                )
            else:
                booking = form.save(commit=False)
                booking.user = request.user
                booking.tour = tour
                booking.status = Booking.Status.PENDING
                booking.save()

                messages.success(
                    request,
                    "Booking created and sent for confirmation.",
                )

                return redirect("booking_list")
    else:
        form = BookingForm()

    return render(
        request,
        "tours/booking_form.html",
        {
            "form": form,
            "tour": tour,
            "title": "Book tour",
        },
    )


@login_required
def booking_list(request):
    bookings = (
        Booking.objects
        .filter(user=request.user)
        .select_related(
            "tour",
            "tour__country",
        )
    )

    return render(
        request,
        "tours/booking_list.html",
        {"bookings": bookings},
    )


@login_required
def edit_booking(request, pk):
    booking = get_object_or_404(
        Booking.objects.select_related("tour"),
        pk=pk,
        user=request.user,
    )

    if booking.status != Booking.Status.PENDING:
        messages.warning(
            request,
            "Only pending bookings can be edited.",
        )
        return redirect("booking_list")

    if not booking.tour.is_active or booking.tour.start_date <= timezone.localdate():
        messages.warning(request, "This tour can no longer be modified.")
        return redirect("booking_list")

    if request.method == "POST":
        form = BookingForm(
            request.POST,
            instance=booking,
        )

        if form.is_valid():
            persons = form.cleaned_data["persons"]

            if persons > booking.tour.available_seats:
                form.add_error(
                    "persons",
                    f"Only {booking.tour.available_seats} seats are available.",
                )
            else:
                form.save()

                messages.success(
                    request,
                    "Booking updated.",
                )

                return redirect("booking_list")
    else:
        form = BookingForm(instance=booking)

    return render(
        request,
        "tours/booking_form.html",
        {
            "form": form,
            "tour": booking.tour,
            "title": "Edit booking",
        },
    )


@login_required
def delete_booking(request, pk):
    booking = get_object_or_404(
        Booking,
        pk=pk,
        user=request.user,
    )

    if booking.status != Booking.Status.PENDING:
        messages.warning(
            request,
            "Only pending bookings can be deleted.",
        )
        return redirect("booking_list")

    if request.method == "POST":
        booking.delete()

        messages.success(
            request,
            "Booking deleted.",
        )

        return redirect("booking_list")

    return render(
        request,
        "tours/booking_confirm_delete.html",
        {"booking": booking},
    )


@login_required
def create_review(request, pk):
    tour = get_object_or_404(
        Tour,
        pk=pk,
    )

    if tour.end_date >= timezone.localdate():
        messages.warning(request, "Reviews are available after the tour ends.")
        return redirect("tour_detail", pk=tour.pk)

    has_confirmed_booking = Booking.objects.filter(
        user=request.user,
        tour=tour,
        status=Booking.Status.CONFIRMED,
    ).exists()

    if not has_confirmed_booking:
        messages.warning(
            request,
            "You can review only tours with a confirmed booking.",
        )
        return redirect("tour_detail", pk=tour.pk)

    if Review.objects.filter(
        user=request.user,
        tour=tour,
    ).exists():
        messages.warning(
            request,
            "You have already reviewed this tour.",
        )
        return redirect("tour_detail", pk=tour.pk)

    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.tour = tour
            review.save()

            messages.success(
                request,
                "Review added.",
            )

            return redirect(
                "tour_detail",
                pk=tour.pk,
            )
    else:
        form = ReviewForm()

    return render(
        request,
        "tours/review_form.html",
        {
            "form": form,
            "tour": tour,
        },
    )


def staff_required(view):
    return user_passes_test(
        lambda user: user.is_staff
    )(view)


@staff_required
def staff_dashboard(request):
    pending_bookings = (
        Booking.objects
        .filter(
            status=Booking.Status.PENDING
        )
        .select_related(
            "user",
            "tour",
            "tour__country",
        )
        .order_by("created_at")
    )

    revenue_expression = ExpressionWrapper(
        F("bookings__persons") * F("price"),
        output_field=DecimalField(
            max_digits=14,
            decimal_places=2,
        ),
    )

    sales = (
        Tour.objects
        .filter(
            bookings__status=Booking.Status.CONFIRMED
        )
        .values("country__name")
        .annotate(
            sold_bookings=Count("bookings"),
            sold_places=Sum("bookings__persons"),
            revenue=Sum(revenue_expression),
        )
        .order_by("country__name")
    )

    return render(
        request,
        "tours/staff_dashboard.html",
        {
            "pending_bookings": pending_bookings,
            "sales": sales,
        },
    )


@staff_required
@transaction.atomic
def confirm_booking(request, pk):
    booking = get_object_or_404(
        Booking.objects.select_for_update(),
        pk=pk,
    )

    if request.method != "POST":
        return redirect("staff_dashboard")

    if booking.status != Booking.Status.PENDING:
        messages.warning(
            request,
            "This booking has already been processed.",
        )
        return redirect("staff_dashboard")

    tour = Tour.objects.select_for_update().get(
        pk=booking.tour_id
    )

    if booking.persons > tour.available_seats:
        messages.error(
            request,
            f"Cannot confirm booking. Only {tour.available_seats} seats remain.",
        )
        return redirect("staff_dashboard")

    tour.available_seats -= booking.persons
    tour.save(
        update_fields=["available_seats"]
    )

    booking.status = Booking.Status.CONFIRMED
    booking.save(
        update_fields=["status"]
    )

    messages.success(
        request,
        "Booking confirmed.",
    )

    return redirect("staff_dashboard")


@staff_required
@transaction.atomic
def cancel_booking_staff(request, pk):
    booking = get_object_or_404(
        Booking.objects.select_for_update(),
        pk=pk,
    )

    if request.method != "POST":
        return redirect("staff_dashboard")

    if booking.status == Booking.Status.CONFIRMED:
        tour = Tour.objects.select_for_update().get(
            pk=booking.tour_id
        )

        tour.available_seats += booking.persons
        tour.save(
            update_fields=["available_seats"]
        )

    booking.status = Booking.Status.CANCELLED
    booking.save(
        update_fields=["status"]
    )

    messages.success(
        request,
        "Booking cancelled.",
    )

    return redirect("staff_dashboard")


def sold_tours(request):
    sales = (
        Booking.objects
        .filter(status=Booking.Status.CONFIRMED)
        .values(
            "tour_id",
            "tour__title",
            "tour__country__name",
            "tour__price",
        )
        .annotate(
            bookings_count=Count("id"),
            places_sold=Sum("persons"),
            revenue=Sum(
                F("persons") * F("tour__price"),
                output_field=DecimalField(
                    max_digits=14,
                    decimal_places=2,
                ),
            ),
        )
        .order_by("tour__country__name", "tour__title")
    )

    return render(
        request,
        "tours/sold_tours.html",
        {"sales": sales},
    )
