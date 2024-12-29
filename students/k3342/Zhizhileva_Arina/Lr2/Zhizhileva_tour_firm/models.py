from django.contrib.auth.models import User
from django.db import models
from django.db.models import F, Avg

class TourAgency(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    website = models.URLField()
    country = models.CharField(max_length=100, null=True)

class Tour(models.Model):
    name = models.CharField(max_length=255)
    agency = models.ForeignKey(TourAgency, on_delete=models.CASCADE, related_name='tours')
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    payment_conditions = models.TextField()
    available_seats = models.PositiveIntegerField(default=10)
    average_rating = models.FloatField(null=True, blank=True)

    def update_average_rating(self):
        average = self.reviews.aggregate(average=Avg('rating'))['average']
        self.average_rating = average if average is not None else None
        self.save(update_fields=['average_rating'])

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='bookings')
    date_reserved = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
    number_of_seats = models.PositiveIntegerField(default=1)

    class Meta:
        permissions = [
            ("can_confirm_booking", "Can confirm booking"),
        ]

    def save(self, *args, **kwargs):
        if not self.pk:
            original_confirmed = False
        else:
            original_confirmed = Booking.objects.filter(pk=self.pk).values('is_confirmed').first()['is_confirmed']

        if self.is_confirmed and not original_confirmed:
            if self.tour.available_seats > 0:
                self.tour.available_seats = F('available_seats') - 1
                self.tour.save(update_fields=['available_seats'])
            else:
                raise ValueError("No available seats left for this tour.")

        super().save(*args, **kwargs)

class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.tour.update_average_rating()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.tour.update_average_rating()