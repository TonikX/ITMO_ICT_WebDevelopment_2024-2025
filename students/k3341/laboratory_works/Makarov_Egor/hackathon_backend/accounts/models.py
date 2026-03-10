from django.db import models
from django.contrib.auth.models import User

class UserRole(models.TextChoices):
    # Главный администратор
    ADMIN = "ADMIN", "Главный администратор"
    # Жюри
    JURY = "JURY", "Жюри"
    # Куратор задач
    CURATOR = "CURATOR", "Куратор"
    # Капитан команды
    CAPTAIN = "CAPTAIN", "Капитан"

class UserProfile(models.Model):
    """Профиль пользователя с ролью.

    Важно: используем related_name, чтобы удобно делать запросы через user.profile
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.CAPTAIN)

    full_name = models.CharField(max_length=255, blank=True)
    organization = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
