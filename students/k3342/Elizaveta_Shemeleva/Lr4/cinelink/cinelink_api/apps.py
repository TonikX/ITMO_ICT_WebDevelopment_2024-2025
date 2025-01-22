from django.apps import AppConfig


class CinelinkApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cinelink_api"

    def ready(self):
        pass
