from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from lr2.settings import Statuses
import hashlib
import datetime


class Class(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Student(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=256)
    name = models.CharField(max_length=40)
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    def set_password(self, raw_password):
        hashed_password = hashlib.sha256(raw_password.encode('utf-8')).hexdigest()
        self.password = hashed_password

    def check_password(self, raw_password):
        return hashlib.sha256(raw_password.encode('utf-8')).hexdigest() == self.password


class Task(models.Model):
    title = models.TextField()
    description = models.TextField()
    created_at = models.DateField()
    expire_at = models.DateField()
    author = models.CharField(max_length=100)
    student_classes = models.ManyToManyField(Class)

    def __str__(self):
        return self.title

    @property
    def is_past_due(self):
        return datetime.date.today() > self.expire_at


class Assignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    text = models.TextField()
    grade = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5),
    ], null=True, blank=True)
    graded_at = models.DateField(null=True, blank=True)
    received_at = models.DateField()

    status = models.IntegerField(validators=[
        MinValueValidator(min(Statuses)),
        MaxValueValidator(max(Statuses)),
    ], default=1)

    class Meta:
        unique_together = ('task', 'student')

    def __str__(self):
        return f'{self.student.name}: {self.task.title}'
