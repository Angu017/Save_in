from django.forms import ModelForm
from .models import Producto
from django import forms
from .models import UserProfile
from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import UserProfile


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'stock', 'descripcion', 'marca']

    # Validación para el campo 'nombre'
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre:
            raise forms.ValidationError('El nombre del producto no puede estar vacío.')
        return nombre

    # Validación para el campo 'precio'
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is None or precio <= 0:
            raise forms.ValidationError('El precio debe ser un número mayor que cero.')
        return precio

    # Validación para el campo 'stock'
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is None or stock < 0:
            raise forms.ValidationError('El stock no puede ser negativo.')
        return stock

    # Validación para el campo 'marca'
    def clean_marca(self):
        marca = self.cleaned_data.get('marca')
        if not marca:
            raise forms.ValidationError('La marca del producto no puede estar vacía.')
        return marca
    
# Formulario para editar el UserProfile
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role', 'phone', 'address', 'first_name', 'last_name', 'email']

# Formulario para editar los datos del usuario (como el nombre de usuario)
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email']  # O los campos que desees permitir editar

# Formulario para cambiar la contraseña
class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User