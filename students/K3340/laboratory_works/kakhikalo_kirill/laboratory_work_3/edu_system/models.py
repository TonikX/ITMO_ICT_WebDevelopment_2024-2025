from django.db import models


class EducationProgram(models.Model):
    programm_code = models.CharField(
        primary_key=True,
        max_length=16
    )
    programm_type = models.CharField(max_length=16)
    duration = models.SmallIntegerField()

    disciplines = models.ManyToManyField(
        'AcademicDiscipline',
        through='ProgramElement',
        related_name='programs'
    )

    def __str__(self):
        return f"{self.programm_code}"


class AcademicDiscipline(models.Model):
    discipline_id = models.CharField(
        primary_key=True,
        max_length=16
    )
    discipline_name = models.CharField(max_length=128)
    practice_duration = models.IntegerField()
    total_duration = models.IntegerField()
    attestation_type = models.CharField(max_length=16)

    def __str__(self):
        return self.discipline_name


class ProgramElement(models.Model):
    programm_code = models.ForeignKey(
        EducationProgram,
        on_delete=models.CASCADE,
        db_column='programm_code'
    )

    discipline = models.ForeignKey(
        AcademicDiscipline,
        on_delete=models.CASCADE,
        db_column='discipline_id'
    )

    class Meta:
        unique_together = (('programm_code', 'discipline'),)

    def __str__(self):
        return f"{self.programm_code} - {self.discipline}"


class Group(models.Model):
    group_id = models.CharField(
        primary_key=True,
        max_length=8
    )
    programm_code = models.ForeignKey(
        EducationProgram,
        on_delete=models.CASCADE,
        db_column='programm_code'
    )

    maximum_students_amount = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.group_id


class Student(models.Model):
    student_id = models.CharField(
        primary_key=True,
        max_length=16
    )
    group_id = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        db_column='group_id'
    )
    fio = models.CharField(max_length=128)
    contact = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.fio} ({self.student_id})"


class Classroom(models.Model):
    classroom_id = models.CharField(
        primary_key=True,
        max_length=16
    )
    number = models.IntegerField()
    type = models.CharField(max_length=16)
    address = models.CharField(max_length=64)

    def __str__(self):
        return f"Classroom {self.number}"


class Teacher(models.Model):
    teacher_id = models.CharField(
        primary_key=True,
        max_length=16
    )
    name = models.CharField(max_length=128)
    job_title = models.CharField(max_length=64)

    disciplines = models.ManyToManyField(
        'AcademicDiscipline',
        through='TeachingPermit',
        related_name='teachers'
    )

    def __str__(self):
        return self.name


class ClassSession(models.Model):
    class_id = models.CharField(
        primary_key=True,
        max_length=16
    )
    date = models.DateField()
    classes_order_number = models.IntegerField()
    type = models.CharField(max_length=16)
    group_id = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        db_column='group_id'
    )
    classroom_id = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        db_column='classroom_id'
    )
    teacher_id = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        db_column='teacher_id'
    )
    discipline_id = models.ForeignKey(
        AcademicDiscipline,
        on_delete=models.CASCADE,
        db_column='discipline_id'
    )

    def __str__(self):
        return f"Class {self.class_id} on {self.date}"


class TeachingPermit(models.Model):
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        db_column='teacher_id'
    )
    discipline = models.ForeignKey(
        AcademicDiscipline,
        on_delete=models.CASCADE,
        db_column='discipline_id'
    )

    class Meta:
        unique_together = (('teacher', 'discipline'),)

    def __str__(self):
        return f"{self.teacher} can teach {self.discipline}"


class Result(models.Model):
    result_id = models.CharField(
        primary_key=True,
        max_length=16
    )
    class_id = models.ForeignKey(
        ClassSession,
        on_delete=models.CASCADE,
        db_column='class_id'
    )
    result = models.CharField(max_length=16)
    student_id = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        db_column='student_id'
    )

    def __str__(self):
        return f"Result {self.result_id}"
