from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Group(models.Model):
    group_grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(11)])
    group_name = models.CharField(max_length=1)


class Subject(models.Model):
    subject_name = models.CharField(max_length=50)


class Room(models.Model):
    number = models.CharField(max_length=4)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)


class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.first_name} {self.second_name} {self.patronymic}'


class Schedule(models.Model):
    day_of_week = (
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),
    )
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    number_of_lesson = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    day_of_week = models.CharField(max_length=3, choices=day_of_week)
    time = models.TimeField()


class HomeTeacher(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class Student(models.Model):
    genders = (
        ('m', 'Male'),
        ('f', 'Female'),
    )
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=genders)

    def __str__(self):
        return f'{self.first_name} {self.second_name} {self.patronymic}'


class LessonGrades(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])


class QuarterGrades(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
