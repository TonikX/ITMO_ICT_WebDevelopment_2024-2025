from django.db import models
from django.contrib.auth.models import AbstractUser
from djangoProject import settings


class Class(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.year})"


class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    student_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.get_role_display()})"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    teachers = models.ManyToManyField(User, related_name='subjects', limit_choices_to={'role': 'teacher'})

    def __str__(self):
        return self.name


class Homework(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                limit_choices_to={'role': 'teacher'})
    assigned_date = models.DateField()
    due_date = models.DateField()
    description = models.TextField()
    penalties_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.subject.name} (выдано {self.assigned_date})"


class Submission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                limit_choices_to={'role': 'student'})
    submission_text = models.TextField()
    submission_date = models.DateField(auto_now_add=True)
    grade = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Submission by {self.student} for {self.homework.title}"
