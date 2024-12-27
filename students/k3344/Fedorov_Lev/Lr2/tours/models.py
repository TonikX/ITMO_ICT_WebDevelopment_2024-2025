from django.db import models
from django.contrib.auth.models import User

class Agency(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name="Название агентства")
    contact_info = models.TextField(verbose_name="Контактная информация")

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=255, verbose_name="Страна")

    def __str__(self):
        return self.name

class Tour(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название тура")
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='tours', verbose_name="Турагентство")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='tours', verbose_name="Страна")
    description = models.TextField(verbose_name="Описание тура")
    start_date = models.DateField(verbose_name="Дата начала тура")
    end_date = models.DateField(verbose_name="Дата окончания тура")
    payment_terms = models.TextField(verbose_name="Условия оплаты")

    def __str__(self):
        return self.name

class Booking(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='bookings', verbose_name="Тур")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    reserved_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата резервирования")
    is_confirmed = models.BooleanField(default=False, verbose_name="Подтверждено администратором")

    def __str__(self):
        return f"{self.user.username} - {self.tour.name}"

class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews', verbose_name="Тур")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Комментатор")
    rating = models.PositiveSmallIntegerField(verbose_name="Рейтинг (1-10)", choices=[(i, str(i)) for i in range(1, 11)])
    comment = models.TextField(verbose_name="Текст комментария")
    date = models.DateField(auto_now_add=True, verbose_name="Дата отзыва")

    def __str__(self):
        return f"Review by {self.user.username} on {self.tour.name}"