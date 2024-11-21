from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from .forms import ProductoForm





#Usuario administrador djando: 4dm1n clave: Adm1n
 
# Create your views here.
def index(request):

    return render(request, 'index.html')

def about(request):

    return render(request, 'about.html')

def client(request):

    return render(request, 'client.html')

def log_in(request):

    return render(request, 'log_in.html')

def register(request):

    return render(request, 'register.html')
def adminpage(request):

    return render(request, 'adminpage.html')

def adminusuarios(request):

    return render(request, 'adminusuarios.html')

def inventarioadmin(request):

    return render(request, 'inventarioadmin.html')

def vendedor(request):

    return render(request, 'vendedor.html')

#Funcion de registro de nuevo Usuario
#ademas de la creacion de nuevos usuarios esta contiene los formularios de django para el uso de validaciones del contraseña y que los nombres de usuario no se repitan
#por lo que con esto contamos con validaciones de seguridad y obviamenten los campos no pueden estar vacios
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # Verificar si el formulario es válido
        if form.is_valid():
            # Guardar el nuevo usuario
            user = form.save()
            # Hacer login con el usuario recién creado
            login(request, user)
            return redirect('adminpage')  # redirigir a la página de administración
        else:
            # Si no es válido, mostramos los errores
            return render(request, 'signup.html', {'form': form})
    else:
        # Si la solicitud es GET, mostramos el formulario vacío
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

#Funcion Inicio de Sesion, Aqui crea la funcion de inicio de sesion y utilizamos los formularios de nos da DJango
#Tambien incluimos las validadiones de que los campos no pueden estar vacios para el inicio de sesion, ademas de que si las credenciales son correctas redirecciona a la pagina correspondiente
def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            # Obtener el usuario autenticado
            user = form.get_user()

            # Verificar si el campo de usuario y contraseña no están vacíos
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            if not username or not password:
                return HttpResponse("El campo de usuario y contraseña no puede estar vacío.")
            
            # Verificar si las credenciales son correctas usando `authenticate`
            user = authenticate(username=username, password=password)
            if user is not None:
                # Si está marcado "recordarme"
                remember_me = request.POST.get('remember_me')  # El checkbox se llama 'remember_me'

                if remember_me:
                    # Si está marcado, la sesión durará 2 semanas (default de Django)
                    request.session.set_expiry(1209600)  # 1209600 segundos = 2 semanas
                else:
                    # Si no está marcado, la sesión durará lo normal (hasta que se cierre el navegador)
                    request.session.set_expiry(0)  # 0 significa que la sesión expirará al cerrar el navegador

                # Iniciar sesión del usuario
                login(request, user)
                
                # Redirigir al usuario a la página de adminpage después de iniciar sesión
                return redirect('adminpage')  # Puedes cambiar 'adminpage' por la URL que quieras
            else:
                # Si las credenciales no son correctas, mostrar mensaje de error
                return HttpResponse("Credenciales incorrectas, intente nuevamente.")
        else:
            # Si el formulario no es válido, devolverlo con los errores
            return render(request, 'signin.html', {'form': form})
    
    else:
        # Si es un GET, mostrar el formulario vacío
        form = AuthenticationForm()
        return render(request, 'signin.html', {'form': form})

#Funcion de cerrar cesion
def logout_view(request):
    logout(request)
    return redirect('index')  # Redirige a la página principal

#crear productos
def crearproducto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            # Aquí puedes agregar un mensaje de éxito si lo deseas.
            return render(request, 'crearproducto.html', {'form': ProductoForm(), 'success': True})
    else:
        form = ProductoForm()

    return render(request, 'crearproducto.html', {'form': form})
