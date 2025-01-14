from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
import re


class Tour(models.Model):
    name = models.CharField(max_length=100)
    agency = models.CharField(max_length=100)
    country = models.CharField(max_length=100)  # Новое поле для страны
    description = models.TextField()
    start_date = models.CharField(max_length=5)
    end_date = models.CharField(max_length=5)

    def clean(self):
        date_format = re.compile(r'^\d{2}.\d{2}$')  # Формат 'DD.MM'

        if not date_format.match(self.start_date) or not date_format.match(self.end_date):
            raise ValidationError("Формат даты должен быть 'DD.MM'")

    def __str__(self):
        return self.name

class Reservation(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reservations')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation_date = models.DateField()
    payment_conditions = models.TextField(blank=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.tour.name} - {'Подтверждено' if self.is_confirmed else 'Не подтверждено'}"

class Comment(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    travel_date = models.DateField()  # Дата поездки
    text = models.TextField()  # Текст комментария
    rating = models.PositiveSmallIntegerField()  # Оценка от 1 до 10
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания комментария

    def __str__(self):
        return f"{self.user.username} - {self.tour.name} - {self.rating}/10"