from django.db import models
from django.conf import settings


class TourAgency(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tour(models.Model):
    title = models.CharField(max_length=255)
    agency = models.ForeignKey(TourAgency, on_delete=models.CASCADE, related_name='tours')
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    payment_terms = models.TextField()
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Reservation(models.Model):
    RETURN_POLICY_CHOICES = [
        ('refundable', 'С возможностью возврата'),
        ('non_refundable', 'Без возможности возврата'),
    ]

    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reservations')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    is_confirmed = models.BooleanField(default=False)
    return_policy = models.CharField(max_length=15, choices=RETURN_POLICY_CHOICES, default='refundable')
    participants_count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Бронирование {self.tour.title} пользователем {self.user.username}"


class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)])
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.tour.title}"
