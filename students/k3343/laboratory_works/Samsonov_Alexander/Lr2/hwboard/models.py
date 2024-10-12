from datetime import date

import bcrypt
from django.db import models


# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=256)
    student_class = models.ForeignKey('hwboard.StudentClass', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    def set_password(self, raw_password):
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
        self.password = hashed_password.decode('utf-8')

    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))


class StudentClass(models.Model):
    name = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    issue_date = models.DateField()
    due_date = models.DateField()
    author = models.CharField(max_length=100)
    student_classes = models.ManyToManyField(StudentClass)

    penalties = models.TextField()

    def __str__(self):
        return self.title

    @property
    def is_past_due(self):
        return date.today() > self.due_date


class Assignment(models.Model):
    ASSIGNMENT_STATUSES = {
        'is': 'issued',
        'pd': 'pending',
        'gd': 'graded'
    }

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    text = models.TextField()
    grade = models.IntegerField(null=True, blank=True)
    date_grade = models.DateField(null=True, blank=True)
    date_hand_in = models.DateField()

    status = models.CharField(max_length=2,
                              choices=ASSIGNMENT_STATUSES.items(),
                              default=ASSIGNMENT_STATUSES['is'])

    class Meta:
        unique_together = ('task', 'student')

    def __str__(self):
        return f'{self.task.title} by {self.student.name}'
