from django.db import models


#Super User: Adm1n Password: Adm1n

#Usuario VENDEDOR: juanceto01   Clave: 8ZGf9S7LPEpvrKx
#Usuario DUEÑO: juancarlos Clave: kyuFM5Lrc5YZy6J

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_marca = models.CharField(max_length=500)
    nombre_categoria = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre_categoria


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=500)
    stock = models.IntegerField()
    codigo = models.CharField(max_length=500)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')

    def __str__(self):
        return self.nombre_producto


class Ingreso(models.Model):
    id_ingreso = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    detalle = models.CharField(max_length=1000)
    fecha_ingreso = models.DateField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='ingresos')

    def __str__(self):
        return f"Ingreso {self.id_ingreso} - Producto: {self.producto.nombre_producto}"


class Modificacion(models.Model):
    id_modificacion = models.AutoField(primary_key=True)
    fecha_modificacion = models.DateField()
    razon = models.CharField(max_length=500)
    cantidad_anterior = models.IntegerField()
    nueva_cantidad = models.IntegerField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='modificaciones')

    def __str__(self):
        return f"Modificación {self.id_modificacion} - Producto: {self.producto.nombre_producto}"


class Salida(models.Model):
    salida_id = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    detalle = models.CharField(max_length=1000)
    fecha_salida = models.DateField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='salidas')

    def __str__(self):
        return f"Salida {self.salida_id} - Producto: {self.producto.nombre_producto}"


class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre_rol


class Usuario(models.Model):
    usuario_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=500)
    apellido = models.CharField(max_length=500)
    correo = models.EmailField(max_length=500)
    telefono = models.CharField(max_length=500)
    direccion = models.CharField(max_length=500)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name='usuarios')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Historial(models.Model):
    id_historial = models.AutoField(primary_key=True)
    tipo_movimiento = models.CharField(max_length=500)
    fecha = models.DateField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='historial_productos')
    cantidad = models.IntegerField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='historial_usuarios')
    ingreso = models.ForeignKey(Ingreso, on_delete=models.CASCADE, related_name='historial_ingresos', null=True, blank=True)
    salida = models.ForeignKey(Salida, on_delete=models.CASCADE, related_name='historial_salidas', null=True, blank=True)
    modificacion = models.ForeignKey(Modificacion, on_delete=models.CASCADE, related_name='historial_modificaciones', null=True, blank=True)

    def __str__(self):
        return f"Historial {self.id_historial} - Producto: {self.producto.nombre_producto}"


