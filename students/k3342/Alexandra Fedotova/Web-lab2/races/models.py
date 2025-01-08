from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('participant', 'Участник'),  
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='participant')

    def is_participant(self):
        return self.role == 'participant'

class Team(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Participant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='participant_profile')
    full_name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
    car_description = models.TextField()
    participant_description = models.TextField()
    experience = models.IntegerField()
    race_class = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.full_name} - {self.team}"

class Race(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    result = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Гонка {self.date} в {self.start_time}"

class Registration(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.participant} на {self.race}"

class Comment(models.Model):
    COMMENT_TYPE_CHOICES = [
        ('cooperation', 'Вопрос о сотрудничестве'),
        ('race', 'Вопрос о гонках'),
        ('other', 'Иное')
    ]
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    comment_type = models.CharField(max_length=50, choices=COMMENT_TYPE_CHOICES)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.user} к гонке {self.race} ({self.get_comment_type_display()})"

class RaceResult(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='results')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()  

    class Meta:
        unique_together = ('race', 'team')  
        ordering = ['position']  

    def __str__(self):
        return f"{self.team.name} - Позиция {self.position} в гонке {self.race.date}"