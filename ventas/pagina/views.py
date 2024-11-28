from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import paypalrestsdk
from django.conf import settings
from .forms import ProductoForm, UserProfileForm, CustomUserChangeForm, CustomPasswordChangeForm
from .models import Producto, ProductModificationLog, Marca, Categoria, UserProfile
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.utils.timezone import now
import openpyxl
from django.contrib import messages
from django.utils.timezone import now
import pandas as pd



@login_required
def ver_perfil(request):
    user = request.user
    perfil_data = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    return render(request, 'pagina/ver_perfil.html', {'perfil_data': perfil_data})



def modificarperfil(request):
    return render(request, 'modificarperfil.html')

# Página principal
def index(request):
    return render(request, 'index.html')

# Página "Acerca de"
def about(request):
    return render(request, 'about.html')

# Página del cliente
def client(request):
    return render(request, 'client.html')

# Iniciar sesión
def log_in(request):
    return render(request, 'log_in.html')

# Registrar usuario
def register(request):
    return render(request, 'register.html')

# Página de administración
def adminpage(request):
    return render(request, 'adminpage.html')

# Página de administración de usuarios
def adminusuarios(request):
    return render(request, 'adminusuarios.html')

# Página de inventario para admins
def inventarioadmin(request):
    return render(request, 'inventarioadmin.html')

# Vista Vendedor
@login_required
def vendedor(request):
    productos = Producto.objects.all()

    # Filtros de Marca y Categoría
    marca_id = request.GET.get('marca')
    if marca_id:
        productos = productos.filter(marca_id=marca_id)

    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    # Ordenar por fecha de vencimiento (productos más cercanos a vencer primero)
    productos = productos.order_by('fecha_vencimiento')

    # Paginación
    paginator = Paginator(productos, 15)  # 15 productos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Obtener marcas y categorías para los filtros
    marcas = Marca.objects.all()
    categorias = Categoria.objects.all()

    return render(request, 'vendedor.html', {
        'page_obj': page_obj,
        'marcas': marcas,
        'categorias': categorias
    })

# Función de registro de nuevo Usuario por defecto muestra crear usuarios
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión al registrar
            return redirect('adminpage')  # Redirige a la página de administración después del registro
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})




# Función de registro de nuevo Usuario con el integrado de metodo de pago
#def signup(request):
#    if request.method == 'POST':
#        form = UserCreationForm(request.POST)
#        if form.is_valid():
#            user = form.save()
#            login(request, user)  # Inicia sesión al registrar
#            return redirect('paypal')  # Redirige a la vista de PayPal después del registro
#    else:
#        form = UserCreationForm()
#
#    return render(request, 'signup.html', {'form': form})









# Función de inicio de sesión
def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('adminpage')
        else:
            return render(request, 'signin.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'signin.html', {'form': form})
    



# Función de cierre de sesión
def logout_view(request):
    logout(request)
    return redirect('index')


# Crear nuevo producto
def crearproducto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vendedor')  # Redirige a la lista de productos
    else:
        form = ProductoForm()

    return render(request, 'crearproducto.html', {'form': form})



# Editar producto
@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()  # Guarda los cambios del producto
            return redirect('vendedor')
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'editar_producto.html', {'form': form, 'producto': producto})



# Historial de modificaciones del producto
def historial_modificaciones(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    logs = producto.modification_logs.all().order_by('-fecha_modificacion')
    return render(request, 'historial_modificaciones.html', {'producto': producto, 'logs': logs})



# API de productos (para API externa)
def api_productos(request):
    productos = Producto.objects.all()
    data = [
        {
            "nombre": producto.nombre,
            "stock": producto.stock,
            "precio": producto.precio,
        }
        for producto in productos
    ]
    return JsonResponse(data, safe=False)

# Eliminar producto
@csrf_exempt
def eliminar_producto(request, producto_id):
    if request.method == 'DELETE':
        producto = get_object_or_404(Producto, id=producto_id)
        producto.delete()
        return JsonResponse({'message': 'Producto eliminado correctamente'}, status=200)
    return JsonResponse({'message': 'Método no permitido'}, status=405)

# Mostrar productos con mayor stock
def productos_mayor_stock(request):
    # Obtener los 5 productos con mayor stock
    productos_mayor_stock = Producto.objects.order_by('-stock')[:5]
    productos_fecha_vencimiento = Producto.objects.order_by('fecha_vencimiento')[:5]

    # Crear los datos para los productos con mayor stock
    data_mayor_stock = [
        {
            "id": producto.id,
            "nombre": producto.nombre,
            "marca": producto.marca,
            "categoria": producto.categoria,
            "stock": producto.stock,
        }
        for producto in productos_mayor_stock
    ]

    # Crear los datos para los productos con la fecha de vencimiento más cercana
    data_fecha_vencimiento = [
        {
            "id": producto.id,
            "nombre": producto.nombre,
            "fecha_vencimiento": producto.fecha_vencimiento.strftime('%d/%m/%Y'),
            "stock": producto.stock,
        }
        for producto in productos_fecha_vencimiento
    ]

    print(data_mayor_stock)  # Agregar para depurar
    print(data_fecha_vencimiento)  # Agregar para depurar

    # Retornar ambas listas en un solo JSON
    return JsonResponse({
        "productos_mayor_stock": data_mayor_stock,
        "productos_fecha_vencimiento": data_fecha_vencimiento,
    })

# Configuración de PayPal
paypalrestsdk.configure({
    "mode": "sandbox",  # o "live" para producción
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

# Función para crear la orden de PayPal
def create_paypal_order():
    order = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {
                "total": "10000.00",  # Monto en pesos chilenos
                "currency": "CLP"  # Pesos chilenos
            },
            "description": "Compra de producto"
        }],
        "redirect_urls": {
            "return_url": "http://tu_dominio.com/payment-success",
            "cancel_url": "http://tu_dominio.com/payment-cancelled"
        }
    })

    if order.create():
        return order
    else:
        return None

# Vista para procesar el pago
def process_payment(request):
    if request.method == "POST":
        order = create_paypal_order()
        if order:
            return JsonResponse({'order_id': order.id})
        else:
            return JsonResponse({'error': 'No se pudo crear la orden'}, status=400)
    return render(request, 'paypal.html')

# Vista de éxito del pago
def payment_success(request):
    if request.user.is_authenticated:
        return redirect('adminpage')
    else:
        return redirect('signin')

# Vista para la página de PayPal
def paypal_view(request):
    return render(request, 'paypal.html')  # Renderiza el formulario de PayPal

#modificar perfil
def modificarperfil(request):
    if request.method == 'POST':
        # Obtener los formularios con los datos del POST
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        profile_form = UserProfileForm(request.POST, instance=request.user.profile)

        # Verificar que todos los formularios sean válidos
        if user_form.is_valid() and password_form.is_valid() and profile_form.is_valid():
            # Guardar los cambios en el usuario
            user_form.save()
            
            # Guardar los cambios en la contraseña
            password_form.save()
            
            # Guardar los cambios en el perfil
            profile_form.save()

            # Mantener la sesión activa después de cambiar la contraseña
            update_session_auth_hash(request, password_form.user)
            
            messages.success(request, "¡Perfil y contraseña actualizados con éxito!")
            return redirect('modificarperfil')  # Redirige a la misma página

        else:
            messages.error(request, "Hubo un error al actualizar los datos.")
    else:
        # Si la solicitud es GET, rellenar los formularios con los datos actuales del usuario
        user_form = CustomUserChangeForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)

    return render(request, 'modificarperfil.html', {
        'user_form': user_form,
        'password_form': password_form,
        'profile_form': profile_form,
    })

from django.shortcuts import render
from django.contrib.auth.models import User
#ver perfil
def ver_perfil(request):
    user = request.user
    perfil_data = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    return render(request, 'pagina/ver_perfil.html', {'perfil_data': perfil_data})

# API de productos con la fecha de vencimiento más cercana
def api_productos_fecha_vencimiento(request):
    # Obtener los 5 productos con la fecha de vencimiento más cercana
    productos = Producto.objects.filter(fecha_vencimiento__isnull=False).order_by('fecha_vencimiento')[:5]
    
    data = [
        {
            "id": producto.id,
            "nombre": producto.nombre,
            "fecha_vencimiento": producto.fecha_vencimiento.strftime('%Y-%m-%d'),  # Formato de fecha
            "stock": producto.stock,
        }
        for producto in productos
    ]
    
    return JsonResponse(data, safe=False)


# API de productos con mayor stock
def api_productos_mayor_stock(request):
    # Obtener los 5 productos con mayor stock
    productos = Producto.objects.all().order_by('-stock')[:5]
    
    data = [
        {
            "id": producto.id,
            "nombre": producto.nombre,
            "marca": producto.marca,
            "categoria": producto.categoria,
            "stock": producto.stock,
        }
        for producto in productos
    ]
    
    return JsonResponse(data, safe=False)

#Mostrar las tablas con los productos proximos a vencer y los con mayor stock en la pagina principal
def adminpage(request):
    # Obtener los productos con mayor stock
    productos_mayor_stock = Producto.objects.order_by('-stock')[:5]
    
    # Obtener los productos con la fecha de vencimiento más cercana
    productos_vencimiento = Producto.objects.filter(
        fecha_vencimiento__gte=now()
    ).order_by('fecha_vencimiento')[:5]
    
    # Pasar los datos al template
    return render(request, 'adminpage.html', {
        'productos_mayor_stock': productos_mayor_stock,
        'productos_vencimiento': productos_vencimiento,
    })



def productos_fecha_vencimiento(request):
    productos = Producto.objects.filter(fecha_vencimiento__gte=now()).order_by('fecha_vencimiento')[:5]
    return render(request, 'template.html', {'productos_vencimiento': productos})


def productos_mayor_stock(request):
    productos = Producto.objects.order_by('-stock')[:5]  # Obtén los 5 con mayor stock
    return render(request, 'template.html', {'productos_mayor_stock': productos})






######################################################################################################################################
#Cargar Execel
######################################################################################################################################
def cargar_excel(request):
    if request.method == "POST" and request.FILES["archivo_excel"]:
        archivo = request.FILES["archivo_excel"]
        try:
            # Cargar el archivo Excel
            df = pd.read_excel(archivo)
            
            # Verificar y limpiar los nombres de las columnas
            df.columns = df.columns.str.strip()
            
            # Verificar si las columnas necesarias están presentes
            required_columns = ["Nombre", "Precio", "Descripcion", "Marca", "Categoria", "Fecha Vencimiento", "Stock"]
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return HttpResponse(f"Faltan las siguientes columnas en el archivo Excel: {', '.join(missing_columns)}")

            # Procesar cada fila del Excel
            for index, row in df.iterrows():
                nombre = row["Nombre"]
                precio = row["Precio"]
                descripcion = row["Descripcion"]
                marca_nombre = row["Marca"]
                categoria_nombre = row["Categoria"]
                fecha_vencimiento = row["Fecha Vencimiento"]
                stock = row["Stock"]  # Usar el stock del archivo Excel
                
                # Obtener o crear la marca y categoría si no existen
                marca, created = Marca.objects.get_or_create(nombre=marca_nombre)
                categoria, created = Categoria.objects.get_or_create(nombre=categoria_nombre)
                
                # Crear el producto
                Producto.objects.create(
                    nombre=nombre,
                    precio=precio,
                    descripcion=descripcion,
                    marca=marca,
                    categoria=categoria,
                    fecha_vencimiento=fecha_vencimiento,
                    stock=stock  # Asignar el stock del archivo Excel
                )

            # Redirigir de nuevo a la página de vendedor para actualizar los productos
            return redirect('vendedor')  # Cambia esto al nombre de tu vista de vendedor

        except Exception as e:
            return HttpResponse(f"Error al cargar el archivo: {str(e)}")
    else:
        return HttpResponse("No se ha enviado un archivo válido.")
#######################################################################################################################################    