from django.apps import AppConfig


class HeadTeacherAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "head_teacher_app"

    def ready(self):
        import head_teacher_app.signals
