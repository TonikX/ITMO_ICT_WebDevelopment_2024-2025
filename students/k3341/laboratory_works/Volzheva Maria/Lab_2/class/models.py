from django.db import models
from django.contrib.auth.models import AbstractUser


class Class(models.Model):
    name = models.CharField(max_length=100)

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
    teachers = models.ManyToManyField(User, related_name='subjects', limit_choices_to={'role': 'teacher'})
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Homework(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date_from = models.DateField()
    date_to = models.DateField()  # Изменено на DateField
    description = models.TextField()
    penalties_info = models.TextField(blank=True, null=True)
    classes = models.ManyToManyField(Class, related_name='homeworks', blank=True)

    def __str__(self):
        return f"{self.subject.name} - {self.description[:20]}"


class Submission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Submission by {self.student} for {self.homework}"

    class Meta:
        permissions = [
            ('can_grade_submissions', 'Can grade submissions'),
        ]

