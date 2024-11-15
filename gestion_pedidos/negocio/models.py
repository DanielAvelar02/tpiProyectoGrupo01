from django.db import models
from django.contrib.auth.models import User

class Negocio(models.Model):
    nombre = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/')
    color_primario = models.CharField(max_length=7, default='#FFFFFF', help_text="Código hexadecimal, por ejemplo: #FFFFFF")
    color_secundario = models.CharField(max_length=7, default='#FFFFFF', help_text="Código hexadecimal, por ejemplo: #FFFFFF")
    color_terciario = models.CharField(max_length=7, default='#FFFFFF', help_text="Código hexadecimal, por ejemplo: #FFFFFF")
    slogan = models.CharField(max_length=100)
    programa_lealtad_activado = models.BooleanField(default=True)
    cupones_activado = models.BooleanField(default=True)

class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=50)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE)

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_disponible = models.IntegerField()
    activo = models.BooleanField(default=True)
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE)

class MenuDelDia(models.Model):
    fecha = models.DateField()
    productos = models.ManyToManyField(Producto, through='MenuProducto')

class MenuProducto(models.Model):
    menu = models.ForeignKey(MenuDelDia, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_disponible = models.IntegerField()

class Pedido(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'Cliente'})
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50)
    direccion_entrega = models.CharField(max_length=255)

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

class Repartidor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'Repartidor'})
    estado_activado = models.BooleanField(default=False)

class Fidelizacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'Cliente'})
    tipo = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    vencimiento = models.DateField()
