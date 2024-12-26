from django.db import models
from django.contrib.auth.models import User

class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=100)
    car_description = models.TextField()
    participant_description = models.TextField()
    experience = models.IntegerField()
    participant_class = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.team_name}"


class Race(models.Model):
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    best_time = models.DurationField(null=True, blank=True)  # Лучшее время гонки

    def __str__(self):
        return f"Race on {self.date} at {self.location}"


class RaceResult(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name="results")
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    race_time = models.DurationField()  # Время участника
    position = models.PositiveSmallIntegerField()  # Место участника в гонке

    def __str__(self):
        return f"{self.participant.user.get_full_name()} - {self.race_time}"


class Registration(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.participant.user.get_full_name()} registered for {self.race}"


class Comment(models.Model):
    COMMENT_TYPE_CHOICES = [
        ('cooperation', 'Вопрос о сотрудничестве'),
        ('race', 'Вопрос о гонках'),
        ('other', 'Иное'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Любой пользователь
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    text = models.TextField()
    comment_type = models.CharField(max_length=20, choices=COMMENT_TYPE_CHOICES)
    rating = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.get_full_name()} on {self.race}"
