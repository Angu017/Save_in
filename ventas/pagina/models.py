from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User 
from django.utils import timezone




# Create your models here.

class Marca(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre
    
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre    

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.IntegerField()
    stock = models.IntegerField()
    fechaingreso = models.DateField(default=timezone.now)
    marca = models.ForeignKey('Marca', on_delete=models.PROTECT)
    descripcion = models.TextField(default="Sin descripción")
    
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
    
    
    


