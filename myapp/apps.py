from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'
    
    def ready(self):
        import myapp.signals  # Importa el archivo de señales cuando la aplicación esté lista
