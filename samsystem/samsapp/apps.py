from django.apps import AppConfig

class SamsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'samsapp'

    def ready(self):
        import samsapp.signals  # Ensure signals are registered
