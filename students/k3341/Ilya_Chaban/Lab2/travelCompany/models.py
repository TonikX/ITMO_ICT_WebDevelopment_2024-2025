from django.contrib.auth.models import User
from django.db import models
from django.forms import CharField


class TravelAgency(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    contact_info = models.CharField(max_length=200)
    address = models.CharField(max_length=255, blank=True)
    number = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Tour(models.Model):
    name = models.CharField(max_length=100)
    agency = models.ForeignKey(TravelAgency, on_delete=models.CASCADE, related_name='tours')
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    payment_conditions = models.TextField()
    country = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reservations')
    reservation_date = models.DateField(auto_now=True)
    confirmed = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('canceled', 'Отменено')
    ], default='pending')
    confirmed_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Бронирование для {self.user.username} на тур {self.tour.name}"

class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    date = models.DateField(auto_now_add=True)
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField()


class SoldTour(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    sold_date = models.DateField(auto_now_add=True)