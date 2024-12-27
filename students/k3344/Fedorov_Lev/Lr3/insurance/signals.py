from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .permissions import create_roles_and_permissions


@receiver(post_migrate)
def assign_permissions(sender, **kwargs):
    if sender.name == 'insurance':  # Убедимся, что запускается для конкретного приложения
        create_roles_and_permissions()
