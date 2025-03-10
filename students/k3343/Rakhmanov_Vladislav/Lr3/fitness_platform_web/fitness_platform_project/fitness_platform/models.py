from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True, verbose_name="Name", unique=True)
    email = models.EmailField(unique=True, verbose_name="Email")
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return self.username

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    date = models.DateField()
    weight = models.FloatField()
    notes = models.TextField(blank=True, null=True)

class WorkoutPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_plans')
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Workout(models.Model):
    LEVEL_CHOICES = [('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')]
    TYPE_CHOICES = [('cardio', 'Cardio'), ('strength', 'Strength'), ('flexibility', 'Flexibility')]

    title = models.CharField(max_length=255)
    description = models.TextField()
    video_url = models.URLField()
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    workout_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    duration_minutes = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
