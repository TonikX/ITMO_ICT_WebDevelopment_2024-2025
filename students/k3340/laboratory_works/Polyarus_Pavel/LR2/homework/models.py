from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MinValueValidator

class Subject(models.Model):
    name = models.CharField('Название', max_length=100)
    color = models.CharField(
        'Цвет', max_length=7, default='#007bff', 
        help_text='Цвет в формате HEX, например #FF5733'
    )

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    

class Class(models.Model):
    name = models.CharField('Название класса', max_length=10, unique=True)
    year = models.PositiveIntegerField('Учебный год')
    students = models.ManyToManyField(
        User, 
        related_name='student_classes',
        limit_choices_to={'profile__role': 'student'},
        verbose_name='Студенты',
        blank=True
    )

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.year})"
    

class Homework(models.Model):
    subject = models.ForeignKey(
        Subject, 
        on_delete=models.CASCADE, 
        related_name='homeworks',  # ← Исправлено
        verbose_name='Предмет'
    )

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_homeworks',
        limit_choices_to={'profile__role': 'teacher'},
        verbose_name='Преподаватель'
    )

    classes = models.ManyToManyField(Class, related_name='homeworks', verbose_name='Классы')

    title = models.CharField('Заголовок задания', max_length=100)
    description = models.TextField('Описание задания')
    created_at = models.DateTimeField('Дата выдачи', auto_now_add=True)
    deadline = models.DateTimeField('Срок сдачи')
    max_score = models.PositiveIntegerField('Максимальный балл', default=100)

    class Meta:
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашние задания'
        ordering = ['-created_at']
    
    def get_absolute_url(self):
        return reverse('homework:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.subject.name} - {self.title}"
    
    def is_overdue(self):
        return timezone.now() > self.deadline
    
    def days_overdue(self):
        if not self.is_overdue():
            return 0
        delta = timezone.now() - self.deadline
        return delta.days


class Submission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На проверке'),
        ('graded', 'Проверено'),
        ('revision', 'На доработке'),
    ]
    
    homework = models.ForeignKey(
        Homework,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name='Домашнее задание'
    )
    
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='submissions',
        limit_choices_to={'profile__role': 'student'},
        verbose_name='Студент',
    )

    submitted_at = models.DateTimeField('Дата сдачи', auto_now_add=True)
    answer_text = models.TextField('Текст ответа')

    grade = models.IntegerField('Оценка', null=True, blank=True)
    teacher_comment = models.TextField('Комментарий преподавателя', blank=True)
    
    status = models.CharField(
        'Статус', 
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='pending'
    )

    class Meta:
        verbose_name = 'Сданная работа'
        verbose_name_plural = 'Сданные работы'
        ordering = ['-submitted_at']
        unique_together = ['homework', 'student']

    def __str__(self):
        return f"{self.student.username} - {self.homework.title}"
    
    def calculate_penalty(self):
        """Расчет штрафа: 20 баллов за каждую неделю просрочки"""
        if not self.homework.is_overdue():
            return 0
        
        days_late = (self.submitted_at - self.homework.deadline).days
        weeks_late = days_late // 7
        penalty = weeks_late * 20
        
        return min(penalty, self.homework.max_score)
    
    def final_score(self):
        """Итоговый балл с учетом штрафа"""
        if self.grade is None:
            return None
        
        penalty = self.calculate_penalty()
        final = self.grade - penalty
        
        return max(0, final)
    
    def get_absolute_url(self):
        return reverse('homework:submission_detail', kwargs={'pk': self.pk})