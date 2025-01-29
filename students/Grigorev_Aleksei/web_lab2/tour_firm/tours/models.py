from django.db import models
from django.contrib.auth.models import User

class Tour(models.Model):
    name = models.CharField(max_length=200)
    agency = models.CharField(max_length=200)
    description = models.TextField()
    period = models.CharField(max_length=200)
    payment_conditions = models.TextField()

    def __str__(self):
        return self.name

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    reserved_on = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Бронирование {self.tour.name} для {self.user.username}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    text = models.TextField()  # Текст отзыва
    rating = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.tour.name}"
