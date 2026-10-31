from django.core.exceptions import ValidationError
from decimal import Decimal
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Agency(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=30)
    email = models.EmailField()

    class Meta:
        verbose_name = "Agency"
        verbose_name_plural = "Agencies"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Tour(models.Model):
    agency = models.ForeignKey(
        Agency,
        on_delete=models.CASCADE,
        related_name="tours",
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        related_name="tours",
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    payment_terms = models.TextField(default="Full payment before departure.")
    available_seats = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def clean(self):
        super().clean()
        if (
            self.start_date
            and self.end_date
            and self.end_date < self.start_date
        ):
            raise ValidationError({
                "end_date": "End date cannot be before start date."
            })

    class Meta:
        verbose_name = "Tour"
        verbose_name_plural = "Tours"
        ordering = ["start_date", "title"]

    def __str__(self):
        return f"{self.title} — {self.country}"


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    persons = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} — {self.tour}"

    @property
    def total_price(self):
        return self.tour.price * self.persons


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    tour_start_date = models.DateField()
    tour_end_date = models.DateField()
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ]
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "tour"],
                name="unique_user_tour_review",
            )
        ]

    def __str__(self):
        return f"{self.user} — {self.tour} — {self.rating}/10"

    def save(self, *args, **kwargs):
        if self._state.adding and self.tour_id:
            self.tour_start_date = self.tour.start_date
            self.tour_end_date = self.tour.end_date
        super().save(*args, **kwargs)
