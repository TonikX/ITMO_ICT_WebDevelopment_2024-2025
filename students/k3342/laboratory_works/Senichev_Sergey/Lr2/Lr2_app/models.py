from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    student_class = models.CharField(max_length=50, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.CharField(max_length=100)
    issue_date = models.DateField()
    deadline = models.DateField()
    penalties = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Assignment(models.Model):
    STATUS_CHOICES = [
        ('sb', 'Submitted'),
        ('gr', 'Graded'),
    ]

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    text = models.TextField()
    date_hand_in = models.DateField(auto_now_add=True)
    date_grade = models.DateField(null=True, blank=True)
    grade = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='sb')

    def __str__(self):
        return f"{self.student.name} - {self.task.title}"
