from django.db import models
from django.contrib.auth.models import User


class ClassRoom(models.Model):
    """Кабинеты"""
    room_number = models.PositiveIntegerField(verbose_name="Номер кабинета")
    name = models.CharField(max_length=100, blank=True, verbose_name="Название")
    capacity = models.PositiveIntegerField(blank=True, null=True, verbose_name="Вместимость")

    class Meta:
        verbose_name = "Кабинет"
        verbose_name_plural = "Кабинеты"

    def __str__(self):
        return f"{self.room_number} ({self.name})" if self.name else self.room_number


class Teacher(models.Model):
    """Преподаватели"""
    POSITION_CHOICES = [
        ('преподаватель', 'Преподаватель'),
        ('старший преподаватель', 'Старший преподаватель'),
        ('доцент', 'Доцент'),
        ('профессор', 'Профессор'),
        ('заведующий кафедрой', 'Заведующий кафедрой'),
    ]

    surname = models.CharField(max_length=100, verbose_name="Фамилия")
    name = models.CharField(max_length=100, verbose_name="Имя")
    middle_name = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    position = models.CharField(max_length=50, choices=POSITION_CHOICES, verbose_name="Должность")
    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Закрепленный кабинет"
    )
    is_active = models.BooleanField(default=True, verbose_name="Работает")
    user_account = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Учетная запись"
    )

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"
        ordering = ['surname', 'name']

    def __str__(self):
        return f"{self.surname} {self.name} {self.middle_name}"


class Group(models.Model):
    """Группы студентов"""
    COURSE_CHOICES = [(i, str(i)) for i in range(1, 5)]

    name = models.CharField(max_length=50, unique=True, verbose_name="Название группы")
    course = models.IntegerField(choices=COURSE_CHOICES, verbose_name="Курс")
    specialty = models.CharField(max_length=200, verbose_name="Специальность")
    curator = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Куратор"
    )
    created_year = models.IntegerField(verbose_name="Год создания")

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.name


class Student(models.Model):
    """Студенты"""
    STATUS_CHOICES = [
        ('active', 'Обучается'),
        ('dropped', 'Отчислен'),
        ('academic_leave', 'Академический отпуск'),
        ('graduated', 'Выпустился'),
    ]

    surname = models.CharField(max_length=100, verbose_name="Фамилия")
    name = models.CharField(max_length=100, verbose_name="Имя")
    middle_name = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    group = models.ForeignKey(Group, on_delete=models.PROTECT, verbose_name="Группа")
    enrollment_date = models.DateField(verbose_name="Дата поступления")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name="Статус"
    )
    user_account = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Учетная запись"
    )

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        ordering = ['surname', 'name']

    def __str__(self):
        return f"{self.surname} {self.name} {self.middle_name}"

    def get_full_name(self):
        return f"{self.surname} {self.name} {self.middle_name}"


class Subject(models.Model):
    """Дисциплины"""
    SEMESTER_CHOICES = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'),]

    name = models.CharField(max_length=200, verbose_name="Название дисциплины")
    course = models.IntegerField(choices=Group.COURSE_CHOICES, verbose_name="Курс")
    semester = models.IntegerField(choices=SEMESTER_CHOICES, verbose_name="Семестр")
    hours = models.PositiveIntegerField(verbose_name="Количество часов")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Дисциплина"
        verbose_name_plural = "Дисциплины"
        unique_together = ['name', 'course', 'semester']

    def __str__(self):
        return f"{self.name} ({self.course} курс, {self.semester} семестр)"


class TeacherSubject(models.Model):
    """Преподаватели и дисциплины (многие-ко-многим)"""
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Преподаватель")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Дисциплина")

    class Meta:
        verbose_name = "Преподаватель-дисциплина"
        verbose_name_plural = "Преподаватели-дисциплины"
        unique_together = ['teacher', 'subject']

    def __str__(self):
        return f"{self.teacher} - {self.subject}"


class Schedule(models.Model):
    """Расписание занятий"""
    DAY_CHOICES = [
        (1, 'Понедельник'),
        (2, 'Вторник'),
        (3, 'Среда'),
        (4, 'Четверг'),
        (5, 'Пятница'),
        (6, 'Суббота')
    ]

    LESSON_NUMBER_CHOICES = [(i, f"{i} пара") for i in range(1, 7)]

    LESSON_TYPE_CHOICES = [
        ('lecture', 'Лекция'),
        ('practice', 'Практика'),
        ('lab', 'Лабораторная работа'),
        ('seminar', 'Семинар'),
    ]

    WEEK_TYPE_CHOICES = [
        ('odd', 'Нечетная неделя'),
        ('even', 'Четная неделя'),
        ('both', 'Каждую неделю'),
    ]

    day_of_week = models.IntegerField(choices=DAY_CHOICES, verbose_name="День недели")
    lesson_number = models.IntegerField(choices=LESSON_NUMBER_CHOICES, verbose_name="Номер пары")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Группа")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Дисциплина")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Преподаватель")
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, verbose_name="Кабинет")
    lesson_type = models.CharField(
        max_length=20,
        choices=LESSON_TYPE_CHOICES,
        verbose_name="Тип занятия"
    )
    week_type = models.CharField(
        max_length=10,
        choices=WEEK_TYPE_CHOICES,
        default='both',
        verbose_name="Тип недели"
    )
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")

    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписание"
        ordering = ['day_of_week', 'lesson_number', 'group']

    def __str__(self):
        return f"{self.get_day_of_week_display()} - {self.lesson_number} пара: {self.group} - {self.subject}"


class Grade(models.Model):
    """Оценки студентов"""
    GRADE_CHOICES = [(2, '2'), (3, '3'), (4, '4'), (5, '5')]
    GRADE_TYPE_CHOICES = [
        ('current', 'Текущая'),
        ('semester', 'Семестровая'),
        ('exam', 'Экзамен'),
        ('credit', 'Зачет'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Студент")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Дисциплина")
    grade = models.IntegerField(choices=GRADE_CHOICES, verbose_name="Оценка")
    grade_type = models.CharField(
        max_length=20,
        choices=GRADE_TYPE_CHOICES,
        default='current',
        verbose_name="Тип оценки"
    )
    semester = models.IntegerField(choices=[(i, str(i)) for i in range(1, 9)], verbose_name="Семестр")
    date = models.DateField(verbose_name="Дата оценки")
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Преподаватель"
    )
    comments = models.TextField(blank=True, verbose_name="Комментарии")

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
        ordering = ['-date']

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.grade}"