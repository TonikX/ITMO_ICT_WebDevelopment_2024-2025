from django.contrib import admin
from django.contrib import messages
from django.db import transaction
from .models import Agency, Booking, Country, Review, Tour


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "email"]
    search_fields = ["name", "address"]


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "country",
        "agency",
        "start_date",
        "end_date",
        "price",
        "available_seats",
        "is_active",
    ]
    list_filter = ["country", "agency", "is_active"]
    search_fields = ["title", "description", "country__name"]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        "user", "tour", "persons", "status", "created_at"
    ]
    list_filter = ["status", "tour__country"]
    search_fields = ["user__username", "tour__title"]
    actions = ["confirm_selected", "cancel_selected"]

    def get_readonly_fields(self, request, obj=None):
        fields = ["status", "created_at"]
        if obj is not None:
            fields += ["user", "tour", "persons"]
        return fields

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.action(description="Confirm selected bookings")
    def confirm_selected(self, request, queryset):
        confirmed = 0
        skipped = 0
        insufficient = 0

        for booking_id in list(queryset.values_list("pk", flat=True)):
            with transaction.atomic():
                booking = Booking.objects.select_for_update().get(
                    pk=booking_id
                )

                if booking.status != Booking.Status.PENDING:
                    skipped += 1
                    continue

                tour = Tour.objects.select_for_update().get(
                    pk=booking.tour_id
                )

                if booking.persons > tour.available_seats:
                    insufficient += 1
                    continue

                tour.available_seats -= booking.persons
                tour.save(update_fields=["available_seats"])

                booking.status = Booking.Status.CONFIRMED
                booking.save(update_fields=["status"])
                confirmed += 1

        self.message_user(
            request,
            f"Confirmed: {confirmed}. Already processed: {skipped}. "
            f"Insufficient seats: {insufficient}.",
            level=messages.SUCCESS if confirmed else messages.WARNING,
        )

    @admin.action(description="Cancel selected bookings")
    def cancel_selected(self, request, queryset):
        cancelled = 0

        for booking_id in list(queryset.values_list("pk", flat=True)):
            with transaction.atomic():
                booking = Booking.objects.select_for_update().get(
                    pk=booking_id
                )

                if booking.status == Booking.Status.CANCELLED:
                    continue

                if booking.status == Booking.Status.CONFIRMED:
                    tour = Tour.objects.select_for_update().get(
                        pk=booking.tour_id
                    )
                    tour.available_seats += booking.persons
                    tour.save(update_fields=["available_seats"])

                booking.status = Booking.Status.CANCELLED
                booking.save(update_fields=["status"])
                cancelled += 1

        self.message_user(
            request,
            f"Cancelled bookings: {cancelled}.",
            level=messages.SUCCESS,
        )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "tour", "tour_start_date", "tour_end_date", "rating", "created_at"]
    readonly_fields = ["tour_start_date", "tour_end_date", "created_at"]
    list_filter = ["rating"]
    search_fields = ["user__username", "tour__title", "text"]
