from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. User (Пользователь)
class User(AbstractUser):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('trainer', 'Trainer'),
    ]
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.full_name

# 2. Profile (Профиль пользователя)
class Profile(models.Model):
    FITNESS_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.IntegerField()
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    fitness_level = models.CharField(max_length=15, choices=FITNESS_LEVEL_CHOICES)
    goals = models.TextField()
    progress = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.full_name}'s Profile"


# 3. Workout (Тренировка)
class Workout(models.Model):
    WORKOUT_TYPE_CHOICES = [
        ('cardio', 'Cardio'),
        ('strength', 'Strength'),
        ('stretching', 'Stretching'),
        ('flexibility', 'Flexibility'),
    ]
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=WORKOUT_TYPE_CHOICES)
    level = models.CharField(max_length=15, choices=LEVEL_CHOICES)
    duration = models.TimeField()
    video_url = models.URLField(max_length=255)
    description = models.TextField()
    instructions = models.TextField()

    def __str__(self):
        return self.title


# 4. Workout_Plan (План тренировок)
class WorkoutPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_plans')
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='workout_plans')
    scheduled_date = models.DateField()

    def __str__(self):
        return f"Plan for {self.user.full_name} on {self.scheduled_date}"


# 5. Blog_Post (Пост в блоге)
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# 6. Progress_Tracking (Отслеживание прогресса)
class ProgressTracking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress_tracking')
    date = models.DateField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    body_fat_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    muscle_mass = models.DecimalField(max_digits=5, decimal_places=2)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Progress on {self.date} for {self.user.full_name}"
