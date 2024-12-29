from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Subject(models.Model):
  name = models.CharField(max_length=50)

  def __str__(self):
    return self.name

class Teacher(models.Model):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  classroom = models.PositiveSmallIntegerField(blank=True, null=True)
  subjects = models.ManyToManyField(Subject, through='TeacherSubject', blank=True)

  def __str__(self):
    return f'{self.first_name} {self.last_name}'

class TeacherSubject(models.Model):
  teacher = models.ForeignKey(Teacher, models.CASCADE)
  subject = models.ForeignKey(Subject, models.CASCADE)

class Grade(models.Model):
  number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(11)])
  letter = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')])
  teacher = models.ForeignKey(Teacher, models.SET_NULL, null=True)

  def __str__(self):
    return f'{self.number}{self.letter}'

class Student(models.Model):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
  grade = models.ForeignKey(Grade, models.CASCADE)
  marks = models.ManyToManyField(Subject, through='Mark', blank=True)

  def __str__(self):
    return f'{self.first_name} {self.last_name}'

class Mark(models.Model):
  student = models.ForeignKey(Student, models.CASCADE)
  subject = models.ForeignKey(Subject, models.CASCADE)
  mark = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])

class Lesson(models.Model):
  grade = models.ForeignKey(Grade, models.CASCADE)
  subject = models.ForeignKey(Subject, models.CASCADE)
  teacher = models.ForeignKey(Teacher, models.CASCADE)
  day_of_week = models.PositiveSmallIntegerField(
    choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday')]
  )
  number = models.SmallIntegerField()

  class Meta:
    unique_together = ('grade', 'day_of_week', 'number')
  
  def __str__(self):
    return f'{self.grade}. {self.day_of_week}, {self.number} lesson - {self.subject}'