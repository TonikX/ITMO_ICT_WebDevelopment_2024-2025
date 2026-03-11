from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        # импортируем сигналы, чтобы автоматически создавать профиль
        from . import signals
