from .models import Producto, ProductModificationLog

def modificar_producto_stock(producto_id, nuevo_stock, usuario, razon=""):
    try:
        producto = Producto.objects.get(id=producto_id)
        
        # Crear registro de modificación
        ProductModificationLog.objects.create(
            producto=producto,
            usuario=usuario,
            stock_anterior=producto.stock,
            stock_nuevo=nuevo_stock,
            razon=razon
        )
        
        # Actualizar el producto
        producto.stock = nuevo_stock
        producto.save()
        print("Modificación registrada con éxito.")
    
    except Producto.DoesNotExist:
        print("Producto no encontrado.")
