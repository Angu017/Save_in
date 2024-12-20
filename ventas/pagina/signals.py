from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile


# Crear perfil de usuario cuando se crea un usuario
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Verificar si el perfil ya existe antes de crear uno nuevo
        if not hasattr(instance, 'profile'):
            UserProfile.objects.create(user=instance)

# Guardar perfil de usuario cuando se guarda un usuario
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Solo guardar el perfil si existe
    if hasattr(instance, 'profile'):
        instance.profile.save()


        
