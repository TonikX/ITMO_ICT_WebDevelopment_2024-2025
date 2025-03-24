from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название предмета")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"


class Assignment(models.Model):
    STATUS_CHOICES = [
        (True, "Активно"),
        (False, "Завершено")
    ]
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True}, verbose_name="Преподаватель")
    issue_date = models.DateTimeField(verbose_name="Дата выдачи")
    due_date = models.DateTimeField(verbose_name="Дата сдачи")
    task_text = models.TextField(verbose_name="Текст задания")
    penalty_info = models.TextField(null=True, blank=True, verbose_name="Информация о штрафах")
    assignment_status = models.BooleanField(default=True, choices=STATUS_CHOICES, verbose_name="Статус задания")

    def __str__(self):
        return f"{self.subject} ({self.issue_date.strftime('%d.%m.%Y')})"

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"


class HomeworkSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, verbose_name="Задание")
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': False}, verbose_name="Ученик")
    submission_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата сдачи")
    text_submission = models.TextField(verbose_name="Ответ ученика")
    grade = models.FloatField(null=True, blank=True, verbose_name="Оценка")

    def __str__(self):
        return f"{self.student.username} → {self.assignment.subject}"

    class Meta:
        verbose_name = "Сдача домашнего задания"
        verbose_name_plural = "Сдачи домашних заданий"
