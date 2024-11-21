from django.contrib import admin
from django.urls import path
from .views import index, about, client, log_in, register, adminpage, adminusuarios, inventarioadmin, vendedor, signup, signin, logout_view, crearproducto, historial_modificaciones, mostrar_productos, api_productos,  eliminar_producto, listar_productos, eliminar_producto
from .views import mostrar_productos





urlpatterns = [
    path('', index, name="index"),
    path('logout/', logout_view, name='logout'),  
    path('about/', about, name="about"),
    path('client/', client, name="client"),
    path('log_in/', log_in, name="log_in"),
    path('register/', register, name="register"),
    path('adminpage/', adminpage, name="adminpage"),
    path('adminusuarios/', adminusuarios, name="adminusuarios"),
    path('inventarioadmin/', inventarioadmin, name="inventarioadmin"),
    path('vendedor/', vendedor, name="vendedor"),
    path('signup/', signup, name="signup"),
    path('signin/', signin, name="signin"),
    path('crearproducto/', crearproducto, name="crearproducto"),
    path('historial-modificaciones/<int:producto_id>/', historial_modificaciones, name='historial_modificaciones'),
    path('productos/', mostrar_productos, name='mostrar_productos'),
    path('api/productos/', api_productos, name='api_productos'),
    path('eliminar-producto/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),
    path('productos/', listar_productos, name='listar_productos'),
    path('eliminar_producto/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),
]
