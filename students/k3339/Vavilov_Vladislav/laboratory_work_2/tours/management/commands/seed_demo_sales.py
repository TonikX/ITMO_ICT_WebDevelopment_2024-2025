from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from tours.models import Booking, Review, Tour


class Command(BaseCommand):
    help = "Create repeatable demonstration bookings, sales and a completed-tour review."

    @transaction.atomic
    def handle(self, *args, **options):
        user, created = get_user_model().objects.get_or_create(
            username="travelway_demo",
            defaults={"email": "demo@example.com"},
        )
        if created:
            user.set_unusable_password()
            user.save(update_fields=["password"])

        created_sales = 0
        for tour_id, persons in [(1, 1), (2, 2), (3, 1), (4, 2), (5, 1)]:
            tour = Tour.objects.select_for_update().get(pk=tour_id)
            booking, booking_created = Booking.objects.get_or_create(
                user=user,
                tour=tour,
                defaults={"persons": persons, "status": Booking.Status.CONFIRMED},
            )
            if booking_created:
                if tour.available_seats < persons:
                    raise ValueError(f"Not enough seats for tour {tour_id}.")
                tour.available_seats -= persons
                tour.save(update_fields=["available_seats"])
                created_sales += 1

        completed_tour = Tour.objects.get(pk=5)
        Review.objects.get_or_create(
            user=user,
            tour=completed_tour,
            defaults={
                "rating": 9,
                "text": "Beautiful scenery, a well-organized trip and a wonderful guide.",
            },
        )
        self.stdout.write(self.style.SUCCESS(f"Added {created_sales} confirmed demo bookings."))
