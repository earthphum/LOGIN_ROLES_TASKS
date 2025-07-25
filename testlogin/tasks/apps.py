from django.apps import AppConfig


class TasksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tasks"

    def ready(self):
        # Import signals ที่นี่เพื่อให้ Django รู้จัก
        import tasks.signals
