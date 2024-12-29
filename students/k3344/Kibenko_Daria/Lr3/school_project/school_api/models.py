from django.db import models

# Модель для предметов
class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Модель для классов
class Classroom(models.Model):
    name = models.CharField(max_length=50, default='Не указано')  # Значение по умолчанию
    is_specialized = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# Модель для учебных классов (классов в школе)
class SchoolClass(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    class_teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

# Модель для учеников
class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1)  # 'M' или 'F'
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    classroom = models.ForeignKey('SchoolClass', on_delete=models.CASCADE)  # Ссылаемся на SchoolClass

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

# Модель для учителей
class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    has_own_class = models.BooleanField(default=False)
    classroom = models.ForeignKey('SchoolClass', null=True, blank=True, on_delete=models.SET_NULL)  # Ссылаемся на SchoolClass

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

# Модель для оценок
class Grade(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)  # Ссылаемся на Subject
    grade = models.DecimalField(max_digits=4, decimal_places=2)
    quarter = models.IntegerField()
    year = models.IntegerField()

    def __str__(self):
        return f'{self.student} - {self.subject} - {self.grade}'

# Модель для расписания
class Schedule(models.Model):
    day_of_week = models.CharField(max_length=20)  # День недели
    lesson_number = models.IntegerField()  # Номер урока
    school_class = models.ForeignKey('SchoolClass', on_delete=models.CASCADE)  # Ссылаемся на SchoolClass
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)  # Ссылаемся на Subject
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)  # Ссылаемся на Teacher
    classroom = models.ForeignKey('Classroom', on_delete=models.SET_NULL, null=True, blank=True)  # Ссылаемся на Classroom

    def __str__(self):
        return f'{self.day_of_week} - {self.lesson_number} - {self.school_class.name} - {self.subject.name}'

