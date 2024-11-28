from django.forms import ModelForm
from .models import Producto, Marca, Categoria
from django import forms
from .models import UserProfile
from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.utils import timezone
from datetime import date


#Formulario Productos
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'stock', 'descripcion', 'marca', 'categoria', 'fecha_vencimiento']
        widgets = {
            'fecha_vencimiento': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'})
        }

    # Los campos de marca y categoria serán de tipo ModelChoiceField
    marca = forms.ModelChoiceField(queryset=Marca.objects.all(), empty_label="Selecciona una marca")
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), required=False, empty_label="Selecciona una categoría")

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre:
            raise forms.ValidationError('El nombre del producto no puede estar vacío.')
        return nombre

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is None or precio <= 0:
            raise forms.ValidationError('El precio debe ser un número mayor que cero.')
        return round(precio, 2)

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is None or stock < 0:
            raise forms.ValidationError('El stock no puede ser negativo.')
        return stock

    def clean_marca(self):
        marca = self.cleaned_data.get('marca')
        if not marca:
            raise forms.ValidationError('La marca del producto no puede estar vacía.')
        return marca

    def clean_categoria(self):
        categoria = self.cleaned_data.get('categoria')
        return categoria

    def clean_fecha_vencimiento(self):
        fecha_vencimiento = self.cleaned_data.get('fecha_vencimiento')

        # Validación para asegurarse de que la fecha no sea anterior a la fecha actual
        if fecha_vencimiento and fecha_vencimiento < timezone.now().date():
            raise forms.ValidationError('La fecha de vencimiento no puede ser anterior a la fecha actual.')

        return fecha_vencimiento
    

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