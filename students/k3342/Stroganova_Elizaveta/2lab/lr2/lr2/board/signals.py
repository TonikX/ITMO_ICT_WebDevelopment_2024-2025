# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Assignment, Journal

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

@receiver(post_save, sender=Assignment)
def update_journal_grade(sender, instance, created, **kwargs):
    # Если задача была обновлена (не создана), обновляем оценку в журнале
    if not created:
        # Найти запись в журнале, которая соответствует студенту и заданию
        try:
            journal_entry = Journal.objects.get(student=instance.student, task=instance.task)
            journal_entry.grade = instance.grade  # Обновляем оценку в журнале
            journal_entry.save()  # Сохраняем изменения в журнале
        except Journal.DoesNotExist:
            # Если записи в журнале нет, создаем новую запись
            Journal.objects.create(student=instance.student, task=instance.task, grade=instance.grade)