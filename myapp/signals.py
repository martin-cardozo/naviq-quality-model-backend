from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import User, Evaluation # Importa el modelo de usuario personalizado desde models.py


@receiver(post_migrate)
def create_initial_users(sender, **kwargs):
    if sender.name == 'myapp':  
        # Verifica si ya existen usuarios en la base de datos
        existing_users = User.objects.filter(email__in=['correo1@example.com', 'correo2@example.com'])
        if not existing_users.exists():
            User.objects.create_user(name='usuario1', email='correo1@example.com', password='contraseña1')
            User.objects.create_user(name='usuario2', email='correo2@example.com', password='contraseña2')
            
            
            
def create_initial_evaluations(sender, **kwargs):
    if sender.name == 'myapp':  
        existing_evaluations = Evaluation.objects.filter(id_evaluation__in=['1'])
        if not existing_evaluations.exists():
            # Crea usuarios de ejemplo solo si no existen
            Evaluation.objects.create_evaluation(
                id_user=1,
                date='2023-09-21',
                result='Resultado 1',
                final_score=90.5,
            )  
        