from django.apps import AppConfig


class MySignalsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_signals'

    def ready(self):
        import my_signals.signals