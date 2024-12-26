from django.db import models
from django.contrib.auth import get_user_model

# Получение кастомной модели пользователя
User = get_user_model()

class Tour(models.Model):
    name = models.CharField(max_length=255)
    agency = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    payment_terms = models.TextField()
    price = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews')  # Привязываем к туру
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Привязываем к пользователю
    rating = models.PositiveIntegerField()  # Оценка от 1 до 5
    comment = models.TextField()  # Текст отзыва
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания отзыва

    def __str__(self):
        return f"Review for {self.tour.name} by {self.user.username}"

class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    tour = models.ForeignKey(to=Tour, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tour.name}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    is_approved = models.BooleanField(default=False)  # Статус подтверждения
    created_at = models.DateTimeField(auto_now_add=True)  # Время создания записи

    def total_price(self):
        return self.quantity * self.tour.price

    def __str__(self):
        return f"Booking: {self.tour.name} by {self.user.username}"
