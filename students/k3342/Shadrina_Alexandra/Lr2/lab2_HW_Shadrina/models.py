from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Create your models here.


class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=7, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.get_role_display()})"


class Homework(models.Model):
    subject = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    assigned_date = models.DateField()
    due_date = models.DateField()
    description = models.TextField()
    penalties = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.subject} (выдано {self.assigned_date})"


class Submission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    submission_text = models.TextField()
    submission_date = models.DateField(auto_now_add=True)
    grade = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.student} - {self.homework}"
