from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from .forms import ProductoForm
from .models import Producto, ProductModificationLog, Marca, Categoria  # Importar Marca y Categoria
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import paypalrestsdk
from django.conf import settings

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

# Página para vendedores
def vendedor(request):
    productos = Producto.objects.all()

    # Filtros de Marca y Categoría
    marca_id = request.GET.get('marca')
    if marca_id:
        productos = productos.filter(marca_id=marca_id)

    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

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

# Función de registro de nuevo Usuario
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión al registrar
            return redirect('paypal')  # Redirige a la vista de PayPal después del registro
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})

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
            return render(request, 'crearproducto.html', {'form': ProductoForm(), 'success': True})
    else:
        form = ProductoForm()
    return render(request, 'crearproducto.html', {'form': form, 'success': False})

# Editar producto
@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            # Guardar el producto con los nuevos datos
            producto = form.save()

            # Obtener el stock anterior y el nuevo
            stock_anterior = producto.stock
            nuevo_stock = form.cleaned_data['stock']

            # Crear un log de la modificación
            ProductModificationLog.objects.create(
                producto=producto,
                usuario=request.user,
                stock_anterior=stock_anterior,
                stock_nuevo=nuevo_stock,
                razon=form.cleaned_data['descripcion']
            )

            return redirect('vendedor')  # Redirige al listado de productos de vendedor
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
    # Obtener los 20 productos con mayor stock
    productos = Producto.objects.order_by('-stock')[:20]
    data = [
        {
            "id": producto.id,
            "nombre": producto.nombre,
            "stock": producto.stock,
        }
        for producto in productos
    ]
    return JsonResponse(data, safe=False)

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
