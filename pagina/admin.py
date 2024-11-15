from django.contrib import admin

# Register your models here.

# inventario/admin.py
#Modificar tablas desde vista admin DJango
from .models import Categoria, Producto, Ingreso, Modificacion, Salida, Usuario, Rol, Historial

# Registra los modelos en el administrador de Django
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Ingreso)       
admin.site.register(Modificacion)
admin.site.register(Salida)         
admin.site.register(Rol)
admin.site.register(Historial)