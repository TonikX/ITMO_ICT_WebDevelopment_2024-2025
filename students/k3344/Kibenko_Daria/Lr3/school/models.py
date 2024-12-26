from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.username


class Classroom(models.Model):
    number = models.CharField(max_length=10)
    is_specialized = models.BooleanField(default=False)

    def __str__(self):
        return self.number


class Subject(models.Model):
    name = models.CharField(max_length=100)
    is_specialized = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    has_own_classroom = models.BooleanField(default=False)
    classroom = models.ForeignKey(Classroom, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Class(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    class_teacher = models.ForeignKey(Teacher, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    DAY_CHOICES = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
    ]
    day_of_week = models.CharField(max_length=3, choices=DAY_CHOICES)
    lesson_number = models.IntegerField()
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('class_instance', 'day_of_week', 'lesson_number')


class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.IntegerField()
    quarter = models.IntegerField()
    year = models.IntegerField()

    class Meta:
        unique_together = ('student', 'subject', 'quarter', 'year')


class ClassTeacher(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        unique_together = ('teacher', 'class_instance')


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
        ('Excused', 'Excused'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE)
    lesson_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)


class DisciplinaryRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    violation_description = models.TextField()
    violation_date = models.DateField()
    punishment = models.TextField()


class Parent(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()


class StudentParent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    relationship = models.CharField(max_length=10)

    class Meta:
        unique_together = ('student', 'parent')