from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.
class Conference(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    event_date = models.DateField()
    due_register = models.DateField()
    participation_condition = models.TextField()

    def __str__(self):
        return self.title


class Speaker(models.Model):
    speaker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.CharField(max_length=100)
    description = models.TextField()
    conference = models.ForeignKey(Conference, on_delete=models.SET_NULL, null=True)

    confirmed = models.BooleanField(default=False)  # You are going to perform
    approved = models.BooleanField(default=None, null=True, blank=True)  # your performance is approved for publishing

    def __str__(self):
        return f'{self.speaker.username}: {self.topic}'


class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    dt_register = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.conference.title}'


class Review(models.Model):
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    text = models.TextField()