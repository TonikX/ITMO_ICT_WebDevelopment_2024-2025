from django.apps import AppConfig

class FitnessPlatformConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "fitness_platform"

    def ready(self):
        from django.contrib.auth.models import AbstractUser 