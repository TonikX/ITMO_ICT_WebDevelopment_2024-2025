from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Racer(models.Model):
    full_name = models.CharField(max_length=150)
    team = models.ForeignKey(Team, related_name='racers', on_delete=models.CASCADE)
    car_description = models.TextField()
    bio = models.TextField()
    experience = models.IntegerField()
    racer_class = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name


class Race(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=100)
    participants = models.ManyToManyField(Racer, related_name='races')

    def __str__(self):
        return f'{self.name} - {self.date}'


class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, related_name='registrations', on_delete=models.CASCADE)
    racer = models.ForeignKey(Racer, related_name='registrations', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Registration of {self.racer.full_name} for {self.race.name}'


class RaceResult(models.Model):
    race = models.ForeignKey(Race, related_name='results', on_delete=models.CASCADE)
    racer = models.ForeignKey(Racer, related_name='race_results', on_delete=models.CASCADE)
    time = models.DurationField()
    result = models.CharField(max_length=100)

    def __str__(self):
        return f'Result of {self.racer.full_name} in {self.race.name}'


class RaceComment(models.Model):
    registration = models.ForeignKey(Registration, related_name='comments', on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_type = models.CharField(
        max_length=50,
        choices=[
            ('cooperation', 'Вопрос о сотрудничестве'),
            ('race', 'Вопрос о гонках'),
            ('other', 'Иное')
        ]
    )
    rating = models.IntegerField()
    race_date = models.DateField()

    def __str__(self):
        return f'Comment by {self.registration.user.username} - Rating {self.rating}'

class User(AbstractUser):
    passport_number = models.CharField(max_length=20, blank=True, null=True)
    home_address = models.TextField(blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.username
