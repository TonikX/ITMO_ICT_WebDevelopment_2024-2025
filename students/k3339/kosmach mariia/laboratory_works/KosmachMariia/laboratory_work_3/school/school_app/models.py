from django.db import models


class Classes(models.Model):
    litera_types = (
        ('A', 'А'),
        ('B', 'Б'),
        ('V', 'В'),
        ('G', 'Г'),
    )
    teacher = models.ForeignKey(
        'Teachers',
        on_delete=models.CASCADE,
        verbose_name='Классный руководитель',
        blank=True,
        null=True
    )
    year = models.IntegerField(verbose_name='Год обучения')
    litera = models.CharField(
        max_length=1,
        choices=litera_types,
        verbose_name='Буква'
    )
    teachings = models.ManyToManyField(
        'Teachings',
        verbose_name='Преподавания',
        through='Schedules',
        related_name='class_teachings'
    )


class Teachers(models.Model):
    cabinet = models.OneToOneField('Cabinets', on_delete=models.CASCADE, primary_key=False, blank=True, null=True)
    FIO = models.CharField(max_length=120, verbose_name='ФИО')
    subjects = models.ManyToManyField(
        'Subjects',
        verbose_name='Предметы',
        through='Teachings',
        related_name='teacher_subjects'
    )


class Cabinets(models.Model):
    number = models.IntegerField(verbose_name='Номер')
    floor = models.IntegerField(verbose_name='Этаж')


class Subjects(models.Model):
    subject_types = (
        ('Math', 'Математика'),
        ('Physics', 'Физика'),
        ('Arts', 'ИЗО'),
        ('Music', 'Музыка'),
        ('Chemisty', 'Химия'),
        ('Sports', 'Физическая культура'),
        ('Russian', 'Русский язык'),
        ('English', 'Английский язык'),
        ('Literature', 'Литература')
    )
    teachers = models.ManyToManyField(
        'Teachers',
        verbose_name='Учителя',
        through='Teachings',
        related_name='subject_teachers'
    )
    subject = models.CharField(max_length=50, choices=subject_types, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')


class Teachings(models.Model):
    teacher = models.ForeignKey('Teachers', verbose_name='Учитель', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subjects', verbose_name='Предмет', on_delete=models.CASCADE)
    experience = models.IntegerField(verbose_name='Стаж')
    classes = models.ManyToManyField(
        'Classes',
        verbose_name='Классы',
        through='Schedules',
        related_name='teaching_classes'
    )

    class Meta:
        unique_together = ('teacher', 'subject')


class Schedules(models.Model):
    teaching = models.ForeignKey(
        'Teachings',
        on_delete=models.CASCADE,
        verbose_name='Преподавание',
        blank=True,
        null=True
    )
    group = models.ForeignKey('Classes', on_delete=models.CASCADE, verbose_name='Класс', blank=True, null=True)
    date = models.DateTimeField()
    students = models.ManyToManyField(
        'Students',
        verbose_name='Ученики',
        through='Grades',
        related_name='schedule_students'
    )


class Students(models.Model):
    group = models.ForeignKey('Classes', on_delete=models.CASCADE, verbose_name='Класс', blank=True, null=True)
    FIO = models.CharField(max_length=120, verbose_name='ФИО')
    schedules = models.ManyToManyField('Schedules', verbose_name='Занятия', through='Grades',
                                       related_name='student_schedules')


class Grades(models.Model):
    grade_types = (
        ('2', 'Неудовлетворительно'),
        ('3', 'Удовлетворительно'),
        ('4', 'Хорошо'),
        ('5', 'Отлично'),
    )
    schedule = models.ForeignKey('Schedules', on_delete=models.CASCADE, verbose_name='Предмет в расписании', blank=True,
                                 null=True)
    student = models.ForeignKey('Students', on_delete=models.CASCADE, verbose_name='Ученик', blank=True, null=True)
    grade = models.CharField(max_length=50, choices=grade_types, verbose_name='Оценка')
    attendance = models.BooleanField(blank=True, null=True)
