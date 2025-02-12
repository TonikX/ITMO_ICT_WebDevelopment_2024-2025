from django.db import models


class Teacher(models.Model):
    """
    Описание учителя
    """
    first_name = models.CharField(max_length=120, verbose_name='Имя')
    last_name = models.CharField(max_length=120, verbose_name='Фамилия')
    subject = models.ManyToManyField('Subject', through='TeacherSubject', verbose_name='Предметы')
    leaded_class = models.ForeignKey(
        'Class', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name='Классный руководитель',
        related_name='led_by_teacher',
        limit_choices_to={'lead_teacher__isnull': False}
    )
    cabinet = models.ForeignKey('Classroom', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Закрепленный кабинет')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Subject(models.Model):
    """
    Описание предмета
    """
    title = models.CharField(max_length=120, verbose_name='Наименование предмета')

    def __str__(self):
        return self.title


class TeacherSubject(models.Model):
    """
    Описание предметов, которые преподавал учитель в определенный период
    """
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, verbose_name='Учитель')
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, verbose_name='Предмет')
    start_date = models.DateField(verbose_name='Дата начала преподавания')
    end_date = models.DateField(verbose_name='Дата окончания преподавания')


class Class(models.Model):
    """
    Описание класса
    """
    name = models.CharField(max_length=50, verbose_name='Класс')
    lead_teacher = models.ForeignKey(
        'Teacher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='classes',
        verbose_name='Классный руководитель'
    )

    def __str__(self):
        return self.name


class Student(models.Model):
    """
    Описание ученика
    """
    gender_types = (
        ('m', 'Мужской'),
        ('f', 'Женский'),
    )
    gender = models.CharField(max_length=1, choices=gender_types, verbose_name='Пол')
    first_name = models.CharField(max_length=120, verbose_name='Имя')
    last_name = models.CharField(max_length=120, verbose_name='Фамилия')
    school_classes = models.ManyToManyField('Class', through='StudentClass', verbose_name='Классы')
    grades = models.ManyToManyField('Subject', through='Grade', verbose_name='Оценки')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class StudentClass(models.Model):
    """
    Ассоциация между учеником и классом с периодом обучения
    """
    student = models.ForeignKey('Student', on_delete=models.CASCADE, verbose_name='Ученик')
    school_class = models.ForeignKey('Class', on_delete=models.CASCADE, verbose_name='Класс')
    start_date = models.DateField(verbose_name='Дата начала обучения')
    end_date = models.DateField(verbose_name='Дата окончания обучения')

    def __str__(self):
        return f"{self.student} - {self.school_class} ({self.start_date} - {self.end_date})"


class Grade(models.Model):
    """
    Описание оценок ученика
    """
    student = models.ForeignKey('Student', on_delete=models.CASCADE, verbose_name='Ученик')
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, verbose_name='Предмет')
    year = models.IntegerField(verbose_name='Учебный год')
    quarter = models.IntegerField(verbose_name='Четверть')
    grade = models.IntegerField(verbose_name='Оценка')

    def __str__(self):
        return f"{self.student} - {self.subject.title} - {self.year} - Четверть {self.quarter} - {self.grade}"


class Classroom(models.Model):
    """
    Описание кабинета
    """
    number = models.CharField(max_length=10, verbose_name='Номер кабинета')
    is_profile = models.BooleanField(default=False, verbose_name='Профильный кабинет')

    def __str__(self):
        profile_status = "Профильный" if self.is_profile else "Непрофильный"
        return f"Кабинет {self.number} - {profile_status}"


class Schedule(models.Model):
    """
    Описание расписания занятий
    """
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, verbose_name='Учитель')
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, verbose_name='Предмет')
    class_group = models.ForeignKey('Class', on_delete=models.CASCADE, verbose_name='Класс')
    classroom = models.ForeignKey('Classroom', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Кабинет')
    day_of_week = models.CharField(max_length=50, verbose_name='День недели')
    time = models.TimeField(verbose_name='Время занятия')

    def __str__(self):
        classroom_info = f"Кабинет {self.classroom}" if self.classroom else "Кабинет не назначен"
        return f"{self.teacher} - {self.subject.title} - {self.class_group} - {classroom_info} - {self.day_of_week} - {self.time}"
