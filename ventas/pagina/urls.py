from django.contrib import admin
from django.urls import path
from .views import index, about, client, log_in, register, adminpage, adminusuarios, inventarioadmin, vendedor, signup, signin, logout_view, crearproducto, editar_producto, historial_modificaciones, api_productos, eliminar_producto, productos_mayor_stock, modificarperfil, api_productos_fecha_vencimiento, api_productos_mayor_stock, cargar_excel, verPerfil, obtener_usuarios, eliminar_usuario, cambiar_rol, perfilad, editarad, paypal


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('client/', client, name='client'),
    path('log_in/', log_in, name='log_in'),
    path('register/', register, name='register'),
    path('adminpage/', adminpage, name='adminpage'),
    path('adminusuarios/', adminusuarios, name='adminusuarios'),
    path('inventarioadmin/', inventarioadmin, name='inventarioadmin'),
    path('vendedor/', vendedor, name='vendedor'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('logout/', logout_view, name='logout'),
    path('crearproducto/', crearproducto, name='crearproducto'),
    path('editarproducto/<int:producto_id>/', editar_producto, name='editar_producto'),
    path('historialmodificaciones/<int:producto_id>/', historial_modificaciones, name='historial_modificaciones'),
    path('eliminar_producto/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),
    path('api/productos_mayor_stock/', productos_mayor_stock, name='productos_mayor_stock'),
    
   
    path('paypal/', paypal, name='paypal'),
    path('modificarperfil/', modificarperfil, name='modificarperfil'),
    path('api/productos/', api_productos, name='api_productos'),
    path('api/productos_fecha_vencimiento/', api_productos_fecha_vencimiento, name='api_productos_fecha_vencimiento'),
    path('api/productos_mayor_stock/', api_productos_mayor_stock, name='api_productos_mayor_stock'),
    path("cargar_excel/", cargar_excel, name="cargar_excel"),
    path('verPerfil/', verPerfil, name='verPerfil'),
    path('api/usuarios/', obtener_usuarios, name='obtener_usuarios'),
    path('api/eliminar_usuario/<str:username>/', eliminar_usuario, name='eliminar_usuario'),
    path('api/usuarios/<str:username>/cambiar_rol/', cambiar_rol, name='cambiar_rol'),
    path('perfilad', perfilad, name='perfilad'),
    path('editarad', editarad, name='editarad'),


]
