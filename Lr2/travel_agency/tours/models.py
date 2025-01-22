from django.db import models
from django.contrib.auth.models import User

class TourAgency(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Tour(models.Model):
    name = models.CharField(max_length=255)
    agency = models.ForeignKey(TourAgency, on_delete=models.CASCADE)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    payment_terms = models.CharField(max_length=255)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def average_rating(self):
        avg = self.reviews.aggregate(models.Avg('rating'))['rating__avg']
        return avg if avg else 0

class Reservation(models.Model):
    tour = models.ForeignKey(Tour, related_name='reservations', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reservations', on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('tour', 'user')  # Запрещает повторные резервирования одного тура пользователем

    def __str__(self):
        return f"Резервирование тура '{self.tour.name}' пользователем {self.user.username}"

class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f"Review by {self.user.username} for {self.tour.name}"