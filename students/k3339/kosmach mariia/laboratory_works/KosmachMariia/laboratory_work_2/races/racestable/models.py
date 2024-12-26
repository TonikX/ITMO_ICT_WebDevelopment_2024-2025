from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    has_racer = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Racer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.CharField(max_length=100)
    car = models.CharField(max_length=100)
    description = models.TextField()
    experience = models.IntegerField()
    type = models.CharField(max_length=100)


class Race(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    winner = models.ForeignKey(Racer, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class RaceConnection(models.Model):
    racer = models.ForeignKey(Racer, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('racer', 'race')


class Comment(models.Model):
    COMMENT_TYPES = (
        ("cooperation", "Сотрудничество"),
        ("race", "Гонка"),
        ("other", "Другое")
    )
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    comment_type = models.CharField(max_length=20, choices=COMMENT_TYPES)
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
