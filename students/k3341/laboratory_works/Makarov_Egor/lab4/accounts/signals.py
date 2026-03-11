from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import UserProfile

@receiver(post_save, sender=User)
def create_profile_for_user(sender, instance, created, **kwargs):
    """Автоматически создаём профиль при создании пользователя.

    при регистрации через Djoser у нас сразу появляется роль.
    По умолчанию роль CAPTAIN (капитан команды).
    """
    if created:
        UserProfile.objects.create(user=instance)
