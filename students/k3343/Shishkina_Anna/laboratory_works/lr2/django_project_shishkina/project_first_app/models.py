from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings


class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'Учитель'),
        ('student', 'Ученик'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student', verbose_name="Роль")


class Homework(models.Model):
    subject = models.CharField(max_length=100, verbose_name="Предмет")
    teacher = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='teacher_homeworks', verbose_name="Преподаватель")
    issue_date = models.DateField(verbose_name="Дата выдачи")
    due_date = models.DateField(verbose_name="Срок выполнения")
    description = models.TextField(verbose_name="Текст задания")
    penalty_info = models.TextField(blank=True, null=True, verbose_name="Информация о штрафах")
    
    
class Submission(models.Model):
    hw = models.ForeignKey(Homework, on_delete=models.CASCADE, verbose_name="Предмет")
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="Студент")
    submission_text = models.TextField(verbose_name="Ответ")
    grade = models.IntegerField(blank=True, null=True, verbose_name="Оценка")

