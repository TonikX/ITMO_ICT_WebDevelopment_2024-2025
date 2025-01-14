from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Team(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Car(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="cars")
    description = models.TextField()
    model = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.model} ({self.team.name})"


class Racer(models.Model):
    STATUS_CHOICES = [
        ('platinum', 'Платиновый'),
        ('gold', 'Золотой'),
        ('silver', 'Серебряный'),
        ('bronze', 'Бронзовый'),
        ('without category', 'Нет категории согласно градации FIA')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    bio = models.TextField()
    years_of_experience = models.PositiveIntegerField()
    participant_class = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='bronze')

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.team.name})"


class Race(models.Model):
    title = models.CharField(max_length=255)
    race_date = models.DateTimeField()
    participants = models.ManyToManyField(Racer, through="RaceParticipant")
    result = models.CharField(max_length=255, blank=True, null=True)
    stream_link = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title


class RaceParticipant(models.Model):
    racer = models.ForeignKey(Racer, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    lap_time = models.DurationField(null=True, blank=True)
    result = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.racer.user.username} - {self.race.title}"


class Fan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} (Fan)"


class Comment(models.Model):
    COMMENT_TYPES = [
        ('cooperation', 'Вопрос о сотрудничестве'),
        ('race', 'Вопрос о гонках'),
        ('other', 'Иное'),
    ]

    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    comment_type = models.CharField(max_length=20, choices=COMMENT_TYPES)
    rating = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.race.title}'



