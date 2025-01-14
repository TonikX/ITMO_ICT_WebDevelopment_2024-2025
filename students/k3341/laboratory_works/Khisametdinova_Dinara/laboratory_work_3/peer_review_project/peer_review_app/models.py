from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    
    role = models.CharField(max_length=50, choices=
                            [('teacher', 'Teacher'), ('student', 'Student')])
    username = models.CharField(max_length=150, blank=True, null=True, verbose_name="Name", unique=True)
    email = models.EmailField(unique=True, verbose_name="Email")

    REQUIRED_FIELDS = ['first_name', 'last_name', 'role', 'email']

    def __str__(self):
        return self.username

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')

class Criterion(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='criteria')

class Option(models.Model):
    content = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='options')

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='submissions')
    content = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    SCORE_CHOICES = [
        ('1', 'Poor'),
        ('2', 'Fair'),
        ('3', 'Good'),
        ('4', 'Very Good'),
        ('5', 'Excellent'),
    ]
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE, related_name='reviews')
    comments = models.TextField()
    score = models.CharField(max_length=1, choices=SCORE_CHOICES)


