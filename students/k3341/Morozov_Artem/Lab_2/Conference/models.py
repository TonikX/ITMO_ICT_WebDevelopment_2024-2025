from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class User(AbstractUser):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    password = models.CharField(max_length=128, verbose_name="Пароль")
    education = models.CharField(max_length=200, blank=True, null=True, verbose_name="Образование")
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Номер телефона")

class Conference(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=100)

class PresentationRegistration(models.Model):
    RECOMMENDATION_CHOICES = [
        ('recommended', 'Рекомендован к публикации'),
        ('not_recommended', 'Не рекомендован к публикации'),
        ('pending', 'На рассмотрении'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    abstract = models.TextField()
    registration_date = models.DateTimeField(auto_now_add=True)
    recommended_for_publication = models.CharField(
        max_length=20,
        choices=RECOMMENDATION_CHOICES,
        default='pending',
        verbose_name="Рекомендация к публикации"
    )

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    date = models.DateTimeField(auto_now_add=True)
