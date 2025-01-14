from django.db import models
from django.contrib.auth.models import AbstractUser


class Class(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    student_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')

    def __str__(self):
        return self.username


class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    teachers = models.ManyToManyField(User, related_name='subjects', limit_choices_to={'role': 'teacher'})

    def __str__(self):
        return self.name


class Assignment(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    from_date = models.DateField(auto_now_add=True)  # Дата выдачи задания
    to_date = models.DateField()  # Дата, до которой задание должно быть выполнено
    text = models.TextField()  # Текст задания
    penalties_info = models.TextField(blank=True, null=True)  # Информация о штрафах
    classes = models.ManyToManyField(Class, related_name='assignments', blank=True)

    def __str__(self):
        return f"{self.subject.name} - {self.from_date}"


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_text = models.TextField()  # Текст выполненного задания
    submission_date = models.DateField(auto_now_add=True)  # Дата сдачи задания
    grade = models.FloatField(blank=True, null=True)  # Оценка за задание

    def __str__(self):
        return f"{self.student.username} - {self.assignment.subject.name} - {self.grade}"
