from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    level = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ['id']




class Workout(models.Model):
    TYPE_CHOICES = [
        ('Cardio', 'Cardio'),
        ('Strength', 'Strength'),
        ('Flexibility', 'Flexibility'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField()
    difficulty = models.IntegerField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    equipment = models.JSONField(
        default=list,
        help_text="Список оборудования как массив JSON",
        blank=True,
        null=True)



class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )

    def __str__(self):
        return f"{self.title} by {self.author.name}"


class UserWorkout(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_workouts'
    )
    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
        related_name='user_completions'
    )
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(blank=True, null=True)
    favourite = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'workout']

