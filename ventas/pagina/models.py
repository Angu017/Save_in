from django.db import models
from django.contrib.auth.models import AbstractUser

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
    fechaingreso = models.DecimalField
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    descripcion = models.TextField(default="Sin descripción")
    def __str__(self):
        return self.nombre


