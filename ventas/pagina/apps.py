from django.apps import AppConfig
from django.apps import AppConfig

class Ventas(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'yourappname'

    def ready(self):
        import yourappname.signals  # Importa los signals

class PaginaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pagina'
