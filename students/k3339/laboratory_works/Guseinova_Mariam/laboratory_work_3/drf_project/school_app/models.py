from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Student(models.Model):
    GENDER_CHOICES = [
        ('М', 'Мужской'),
        ('Ж', 'Женский'),
    ]
    id_student = models.AutoField(primary_key=True)
    surname = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    class_name = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.surname} {self.name} ({self.class_name})"


class Grade(models.Model):
    id_grade = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=30)
    grade = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    quarter = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])

    def __str__(self):
        return f"{self.student} | {self.subject}: {self.grade} (Quarter {self.quarter})"


class StudentSchedule(models.Model):
    id_schedule = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lessons = models.ManyToManyField('Lesson')

    def __str__(self):
        lessons_list = ', '.join(lesson.subject for lesson in self.lessons.all())
        return f"Schedule for {self.student}: {lessons_list}"


class Teacher(models.Model):
    id_teacher = models.AutoField(primary_key=True)
    surname = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    room_assigned = models.ForeignKey(
        'Room', null=True, on_delete=models.SET_NULL, related_name='assigned_teachers'
    )
    lessons = models.ManyToManyField('Lesson', related_name='taught_by', blank=True)

    def __str__(self):
        room_info = f"Room: {self.room_assigned}" if self.room_assigned else "No assigned room"
        return f"{self.surname} {self.name} ({room_info})"


class Room(models.Model):
    ROOM_STATUS_CHOICES = [
        ('Оборудованная', 'Оборудованная'),
        ('Базовая', 'Базовая'),
    ]
    id_room = models.AutoField(primary_key=True)
    number = models.CharField(max_length=20)
    status = models.CharField(max_length=15, choices=ROOM_STATUS_CHOICES)
    teacher = models.ManyToManyField(Teacher, blank=True, related_name='rooms')

    def __str__(self):
        return f"{self.number} ({self.get_status_display()})"


class Lesson(models.Model):
    DAY_CHOICES = [
        ('Понедельник', 'Понедельник'),
        ('Вторник', 'Вторник'),
        ('Среда', 'Среда'),
        ('Четверг', 'Четверг'),
        ('Пятница', 'Пятница'),
        ('Суббота', 'Суббота'),
    ]
    NUM_LESSON = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
    ]
    id_lesson = models.AutoField(primary_key=True)
    day = models.CharField(max_length=20, choices=DAY_CHOICES)
    lesson_number = models.CharField(max_length=2, choices=NUM_LESSON)
    subject = models.CharField(max_length=20)
    class_label = models.CharField(max_length=3)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teaches')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return f"{self.subject} ({self.class_label}) | {self.day} Lesson {self.lesson_number}"
