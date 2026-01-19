from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Group(models.Model):
    group_id = models.AutoField(primary_key=True, verbose_name='ID группы')
    group_name = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Название группы'
    )
    course = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        verbose_name='Курс'
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ['course', 'group_name']

    def __str__(self):
        return self.group_name


class Classroom(models.Model):
    classroom_id = models.AutoField(primary_key=True, verbose_name='ID кабинета')
    classroom_number = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='Номер кабинета'
    )
    building = models.CharField(max_length=20, verbose_name='Корпус')
    capacity = models.PositiveSmallIntegerField(
        default=30,
        verbose_name='Вместимость'
    )
    equipment = models.TextField(blank=True, null=True, verbose_name='Оборудование')

    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'
        ordering = ['building', 'classroom_number']

    def __str__(self):
        return f"{self.building}, каб. {self.classroom_number}"


class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True, verbose_name='ID преподавателя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    patronymic = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Отчество'
    )
    position = models.CharField(
        max_length=100,
        default='Преподаватель',
        verbose_name='Должность'
    )
    degree = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Учёная степень'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        unique=True,
        verbose_name='Телефон'
    )
    email = models.EmailField(
        blank=True,
        null=True,
        unique=True,
        verbose_name='Email'
    )
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='teachers',
        verbose_name='Закреплённый кабинет'
    )

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic or ''}".strip()

    @property
    def full_name(self):
        return str(self)


class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True, verbose_name='ID дисциплины')
    subject_code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Код дисциплины'
    )
    subject_name = models.CharField(max_length=100, verbose_name='Название дисциплины')
    hours_total = models.PositiveSmallIntegerField(
        default=72,
        verbose_name='Общее количество часов'
    )
    hours_lecture = models.PositiveSmallIntegerField(
        default=36,
        verbose_name='Лекционные часы'
    )
    hours_practice = models.PositiveSmallIntegerField(
        default=36,
        verbose_name='Практические часы'
    )

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'
        ordering = ['subject_name']

    def __str__(self):
        return f"{self.subject_code} - {self.subject_name}"


class Student(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активен'),
        ('expelled', 'Отчислен'),
        ('academic', 'Академический отпуск'),
    ]

    student_id = models.AutoField(primary_key=True, verbose_name='ID студента')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    patronymic = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Отчество'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='students',
        verbose_name='Группа'
    )
    enrollment_date = models.DateField(verbose_name='Дата зачисления')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Статус'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Телефон'
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='Email'
    )

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic or ''}".strip()

    @property
    def full_name(self):
        return str(self)


class Schedule(models.Model):
    DAY_CHOICES = [
        (1, 'Понедельник'),
        (2, 'Вторник'),
        (3, 'Среда'),
        (4, 'Четверг'),
        (5, 'Пятница'),
        (6, 'Суббота'),
    ]

    SEMESTER_CHOICES = [
        (1, 'Осенний'),
        (2, 'Весенний'),
    ]

    schedule_id = models.AutoField(primary_key=True, verbose_name='ID расписания')
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name='Группа'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name='Дисциплина'
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name='Преподаватель'
    )
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='schedules',
        verbose_name='Кабинет'
    )
    day_of_week = models.PositiveSmallIntegerField(
        choices=DAY_CHOICES,
        verbose_name='День недели'
    )
    lesson_number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)],
        verbose_name='Номер пары'
    )
    semester = models.PositiveSmallIntegerField(
        choices=SEMESTER_CHOICES,
        verbose_name='Семестр'
    )
    academic_year = models.PositiveIntegerField(
        verbose_name='Учебный год'
    )
    week_type = models.CharField(
        max_length=10,
        choices=[('all', 'Все недели'), ('odd', 'Чётная'), ('even', 'Нечётная')],
        default='all',
        verbose_name='Тип недели'
    )
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата окончания'
    )

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'
        ordering = ['day_of_week', 'lesson_number']
        constraints = [
            models.UniqueConstraint(
                fields=['group', 'day_of_week', 'lesson_number', 'semester', 'academic_year'],
                name='unique_schedule_slot'
            )
        ]

    def __str__(self):
        return f"{self.group} - {self.subject} ({self.get_day_of_week_display()}, {self.lesson_number} пара)"


class Grade(models.Model):
    GRADE_TYPE_CHOICES = [
        ('exam', 'Экзамен'),
        ('test', 'Зачёт'),
        ('coursework', 'Курсовая работа'),
        ('practice', 'Практика'),
        ('test_module', 'Модульный контроль'),
    ]

    grade_id = models.AutoField(primary_key=True, verbose_name='ID оценки')
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='grades',
        verbose_name='Студент'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='grades',
        verbose_name='Дисциплина'
    )
    grade_value = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(2.0), MaxValueValidator(5.0)],
        verbose_name='Оценка'
    )
    grade_type = models.CharField(
        max_length=20,
        choices=GRADE_TYPE_CHOICES,
        default='exam',
        verbose_name='Тип оценки'
    )
    semester = models.PositiveSmallIntegerField(
        choices=[(1, 'Осенний'), (2, 'Весенний')],
        verbose_name='Семестр'
    )
    academic_year = models.PositiveIntegerField(verbose_name='Учебный год')
    date_received = models.DateField(verbose_name='Дата получения', default=timezone.now)
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='given_grades',
        verbose_name='Преподаватель'
    )

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        ordering = ['-academic_year', '-semester', 'date_received']
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'subject', 'semester', 'academic_year'],
                name='unique_grade_per_semester'
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.grade_value}"