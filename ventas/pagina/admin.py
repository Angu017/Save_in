
from .models import Producto
from .models import Marca
from .models import Categoria
from .models import UserProfile
from django.contrib import admin

# Register your models here.
admin.site.register(Producto)
admin.site.register(Marca)
admin.site.register(Categoria)
admin.site.register(UserProfile)