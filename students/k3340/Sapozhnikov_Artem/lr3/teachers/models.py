from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    cabinet = models.CharField(max_length=10, blank=True, null=True)
    subjects = models.ManyToManyField(Subject, through='TeacherSubjectPeriod')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class TeacherSubjectPeriod(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    period = models.CharField(max_length=20)  # например "1 четверть"
