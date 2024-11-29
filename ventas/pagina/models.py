from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User 
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your models here.

def obtener_fecha_actual():
    return timezone.now().date()

class Marca(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=4)
    stock = models.IntegerField()
    descripcion = models.TextField()
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, null=True, blank=True, on_delete=models.SET_NULL)
    fecha_vencimiento = models.DateField(default=timezone.now)

    def __str__(self):
        return self.nombre
    
class ProductModificationLog(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="modification_logs")  # Relación con Producto
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Relación con el usuario
    stock_anterior = models.IntegerField()
    stock_nuevo = models.IntegerField()
    razon = models.TextField(default="No especificada")  # Razón de la modificación
    fecha_modificacion = models.DateTimeField(auto_now_add=True)  # Fecha de la modificación

    def __str__(self):
        return f"Modificación de {self.producto.nombre} por {self.usuario.username} en {self.fecha_modificacion}"

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')  # Relación con User
    role = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('editor', 'Editor'), ('viewer', 'Viewer')], default='viewer')  # Roles
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.user.username

# Señal para crear un perfil automáticamente al crear un usuario
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

    
    
    


