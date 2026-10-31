from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Agency, Booking, Country, Review, Tour


class BookingAdminTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username="testadmin",
            email="admin@example.com",
            password="TestPassword123!",
        )
        self.country = Country.objects.create(name="Italy")
        self.agency = Agency.objects.create(
            name="Test Agency",
            address="Test address",
            phone="+1234567890",
            email="agency@example.com",
        )
        self.tour = Tour.objects.create(
            agency=self.agency,
            country=self.country,
            title="Test Tour",
            description="Test description",
            start_date=timezone.localdate() + timedelta(days=30),
            end_date=timezone.localdate() + timedelta(days=35),
            price=Decimal("1000.00"),
            payment_terms="Full payment before departure.",
            available_seats=3,
        )
        self.booking = Booking.objects.create(
            user=self.admin,
            tour=self.tour,
            persons=2,
        )
        self.client.force_login(self.admin)

    def run_action(self, action, booking):
        return self.client.post(
            reverse("admin:tours_booking_changelist"),
            {
                "action": action,
                "_selected_action": [str(booking.pk)],
            },
        )

    def test_confirm_reduces_seats(self):
        self.run_action("confirm_selected", self.booking)
        self.booking.refresh_from_db()
        self.tour.refresh_from_db()
        self.assertEqual(self.booking.status, Booking.Status.CONFIRMED)
        self.assertEqual(self.tour.available_seats, 1)

    def test_admin_booking_changelist_renders(self):
        response = self.client.get(reverse("admin:tours_booking_changelist"))
        self.assertContains(response, "Confirm selected bookings")

    def test_cancel_restores_seats(self):
        self.run_action("confirm_selected", self.booking)
        self.run_action("cancel_selected", self.booking)
        self.booking.refresh_from_db()
        self.tour.refresh_from_db()
        self.assertEqual(self.booking.status, Booking.Status.CANCELLED)
        self.assertEqual(self.tour.available_seats, 3)

    def test_double_confirmation_does_not_double_charge_seats(self):
        self.run_action("confirm_selected", self.booking)
        self.run_action("confirm_selected", self.booking)
        self.tour.refresh_from_db()
        self.assertEqual(self.tour.available_seats, 1)

    def test_insufficient_seats(self):
        self.booking.persons = 4
        self.booking.save(update_fields=["persons"])
        self.run_action("confirm_selected", self.booking)
        self.booking.refresh_from_db()
        self.tour.refresh_from_db()
        self.assertEqual(self.booking.status, Booking.Status.PENDING)
        self.assertEqual(self.tour.available_seats, 3)

    def test_second_booking_cannot_oversell(self):
        second = Booking.objects.create(
            user=self.admin,
            tour=self.tour,
            persons=2,
        )
        self.run_action("confirm_selected", self.booking)
        self.run_action("confirm_selected", second)
        second.refresh_from_db()
        self.tour.refresh_from_db()
        self.assertEqual(second.status, Booking.Status.PENDING)
        self.assertEqual(self.tour.available_seats, 1)


class TourValidationTests(TestCase):
    def setUp(self):
        country = Country.objects.create(name="Italy")
        agency = Agency.objects.create(
            name="Validation Agency",
            address="Test address",
            phone="+1234567890",
            email="validation@example.com",
        )
        self.tour = Tour.objects.create(
            agency=agency,
            country=country,
            title="Validation Tour",
            description="Test description",
            start_date=timezone.localdate() + timedelta(days=30),
            end_date=timezone.localdate() + timedelta(days=35),
            price=Decimal("1000.00"),
            payment_terms="Full payment before departure.",
            available_seats=3,
        )

    def test_valid_tour(self):
        self.tour.full_clean()

    def test_negative_price_rejected(self):
        self.tour.price = Decimal("-100.00")
        with self.assertRaises(ValidationError) as error:
            self.tour.full_clean()
        self.assertIn("price", error.exception.message_dict)

    def test_zero_price_rejected(self):
        self.tour.price = Decimal("0.00")
        with self.assertRaises(ValidationError) as error:
            self.tour.full_clean()
        self.assertIn("price", error.exception.message_dict)

    def test_end_date_before_start_rejected(self):
        self.tour.end_date = self.tour.start_date - timedelta(days=1)
        with self.assertRaises(ValidationError) as error:
            self.tour.full_clean()
        self.assertIn("end_date", error.exception.message_dict)


class TourFilterTests(TestCase):
    def test_invalid_country(self):
        response = self.client.get("/", {"country": "abc"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<option value="">All countries</option>')

    def test_extremely_large_country(self):
        response = self.client.get("/", {"country": "9" * 5000})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<option value="">All countries</option>')


class CustomerFlowTests(TestCase):
    def setUp(self):
        self.customer = get_user_model().objects.create_user(
            username="customer",
            password="ExampleStrong2026!",
        )
        self.other = get_user_model().objects.create_user(
            username="other",
            password="ExampleStrong2026!",
        )
        self.staff = get_user_model().objects.create_user(
            username="manager",
            password="ExampleStrong2026!",
            is_staff=True,
        )
        self.country = Country.objects.create(name="Japan")
        self.agency = Agency.objects.create(
            name="TravelWay",
            address="Test address",
            phone="+1234567890",
            email="agency@example.com",
        )
        self.future_tour = Tour.objects.create(
            agency=self.agency,
            country=self.country,
            title="Future Tour",
            description="Upcoming trip",
            start_date=timezone.localdate() + timedelta(days=20),
            end_date=timezone.localdate() + timedelta(days=25),
            price=Decimal("500.00"),
            available_seats=5,
        )
        self.past_tour = Tour.objects.create(
            agency=self.agency,
            country=self.country,
            title="Past Tour",
            description="Completed trip",
            start_date=timezone.localdate() - timedelta(days=12),
            end_date=timezone.localdate() - timedelta(days=5),
            price=Decimal("100.00"),
            available_seats=5,
        )

    def test_registration(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newtraveler",
                "email": "new@example.com",
                "password1": "ExampleStrong2026!",
                "password2": "ExampleStrong2026!",
            },
        )
        self.assertRedirects(response, reverse("tour_list"))
        self.assertTrue(get_user_model().objects.filter(username="newtraveler").exists())

    def test_booking_edit_delete_and_user_ownership(self):
        self.client.force_login(self.customer)
        response = self.client.post(
            reverse("create_booking", args=[self.future_tour.pk]),
            {"persons": 2},
        )
        self.assertRedirects(response, reverse("booking_list"))
        booking = Booking.objects.get(user=self.customer)
        response = self.client.post(
            reverse("edit_booking", args=[booking.pk]),
            {"persons": 3},
        )
        self.assertRedirects(response, reverse("booking_list"))
        booking.refresh_from_db()
        self.assertEqual(booking.persons, 3)
        self.client.force_login(self.other)
        self.assertEqual(
            self.client.get(reverse("edit_booking", args=[booking.pk])).status_code,
            404,
        )
        self.client.force_login(self.customer)
        self.client.post(reverse("delete_booking", args=[booking.pk]))
        self.assertFalse(Booking.objects.filter(pk=booking.pk).exists())

    def test_staff_confirmation_and_sales(self):
        booking = Booking.objects.create(
            user=self.customer,
            tour=self.future_tour,
            persons=2,
        )
        self.client.force_login(self.customer)
        self.assertRedirects(self.client.get(reverse("staff_dashboard")), "/login/?next=/staff/")
        self.client.force_login(self.staff)
        dashboard = self.client.get(reverse("staff_dashboard"))
        self.assertContains(dashboard, "Administration", status_code=200)
        self.client.post(reverse("confirm_booking", args=[booking.pk]))
        booking.refresh_from_db()
        self.future_tour.refresh_from_db()
        self.assertEqual(booking.status, Booking.Status.CONFIRMED)
        self.assertEqual(self.future_tour.available_seats, 3)
        sales = self.client.get(reverse("sold_tours"))
        self.assertContains(sales, "Future Tour")
        self.client.post(reverse("cancel_booking_staff", args=[booking.pk]))
        self.future_tour.refresh_from_db()
        self.assertEqual(self.future_tour.available_seats, 5)

    def test_review_only_after_tour_and_dates_are_preserved(self):
        self.client.force_login(self.customer)
        Booking.objects.create(
            user=self.customer,
            tour=self.future_tour,
            status=Booking.Status.CONFIRMED,
        )
        response = self.client.post(
            reverse("create_review", args=[self.future_tour.pk]),
            {"rating": 9, "text": "Too early"},
        )
        self.assertRedirects(response, reverse("tour_detail", args=[self.future_tour.pk]))
        self.assertFalse(Review.objects.exists())
        Booking.objects.create(
            user=self.customer,
            tour=self.past_tour,
            status=Booking.Status.CONFIRMED,
        )
        response = self.client.post(
            reverse("create_review", args=[self.past_tour.pk]),
            {"rating": 10, "text": "Excellent journey"},
        )
        self.assertRedirects(response, reverse("tour_detail", args=[self.past_tour.pk]))
        review = Review.objects.get()
        self.assertEqual(review.tour_start_date, self.past_tour.start_date)
        self.assertEqual(review.tour_end_date, self.past_tour.end_date)
        self.past_tour.start_date -= timedelta(days=1)
        self.past_tour.save(update_fields=["start_date"])
        review.refresh_from_db()
        self.assertNotEqual(review.tour_start_date, self.past_tour.start_date)
        self.client.post(
            reverse("create_review", args=[self.past_tour.pk]),
            {"rating": 1, "text": "Duplicate"},
        )
        self.assertEqual(Review.objects.count(), 1)

    def test_inactive_sold_tour_remains_viewable(self):
        self.past_tour.is_active = False
        self.past_tour.save(update_fields=["is_active"])
        self.assertEqual(
            self.client.get(reverse("tour_detail", args=[self.past_tour.pk])).status_code,
            200,
        )
        self.client.force_login(self.customer)
        self.assertEqual(
            self.client.get(reverse("create_booking", args=[self.past_tour.pk])).status_code,
            404,
        )

    def test_past_tour_does_not_advertise_booking(self):
        response = self.client.get(reverse("tour_detail", args=[self.past_tour.pk]))
        self.assertContains(response, "Tour completed")
        self.assertNotContains(response, "Log in to book")

        self.client.force_login(self.customer)
        response = self.client.get(reverse("tour_detail", args=[self.past_tour.pk]))
        self.assertContains(response, "Tour completed")
        self.assertNotContains(response, "Book this tour")

    def test_future_tour_booking_controls_respect_availability(self):
        url = reverse("tour_detail", args=[self.future_tour.pk])
        self.assertContains(self.client.get(url), "Log in to book")
        self.client.force_login(self.customer)
        self.assertContains(self.client.get(url), "Book this tour")

        self.future_tour.available_seats = 0
        self.future_tour.save(update_fields=["available_seats"])
        response = self.client.get(url)
        self.assertContains(response, "Sold out")
        self.assertNotContains(response, "Book this tour")

        self.future_tour.is_active = False
        self.future_tour.save(update_fields=["is_active"])
        self.assertContains(self.client.get(url), "Booking unavailable")

    def test_review_publication_date_is_formatted(self):
        review = Review.objects.create(
            user=self.customer,
            tour=self.past_tour,
            rating=9,
            text="A lovely trip",
        )
        response = self.client.get(reverse("tour_detail", args=[self.past_tour.pk]))
        self.assertContains(response, review.created_at.strftime("%d.%m.%Y %H:%M"))
        self.assertNotContains(response, str(review.created_at))

    def test_pagination_with_more_than_six_tours(self):
        for number in range(7):
            Tour.objects.create(
                agency=self.agency,
                country=self.country,
                title=f"Extra tour {number}",
                description="A future journey",
                start_date=self.future_tour.start_date,
                end_date=self.future_tour.end_date,
                price=Decimal("120.00"),
                available_seats=10,
            )
        response = self.client.get(reverse("tour_list"), {"page": 2})
        self.assertContains(response, "2 / 2")


class DemonstrationDataTests(TestCase):
    def test_fixture_and_sales_command_are_repeatable(self):
        from django.core.management import call_command

        call_command("loaddata", "fixtures/demo_tours.json", verbosity=0)
        self.assertEqual(Tour.objects.count(), 9)
        self.assertEqual(Country.objects.count(), 4)

        call_command("seed_demo_sales", verbosity=0)
        self.assertEqual(Booking.objects.filter(status=Booking.Status.CONFIRMED).count(), 5)
        self.assertEqual(Review.objects.count(), 1)

        call_command("seed_demo_sales", verbosity=0)
        self.assertEqual(Booking.objects.filter(status=Booking.Status.CONFIRMED).count(), 5)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Tour.objects.get(pk=1).available_seats, 11)
