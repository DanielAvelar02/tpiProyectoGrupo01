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

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    puntos = models.IntegerField(default=0)  # Puntos acumulados por el cliente
    
    def __str__(self):
        return self.user.username

    def agregar_puntos(self, puntos):
        """
        Agrega puntos al perfil del usuario si el programa de lealtad está activo.
        """
        if self.user.negocio.programa_lealtad_activado:
            self.puntos += puntos
            self.save()

    def verificar_vencimiento_puntos(self):
        """
        Aquí puedes agregar lógica si deseas que los puntos tengan una fecha de vencimiento.
        """
        pass

class Cupon(models.Model):
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=50, unique=True)
    descuento = models.DecimalField(max_digits=5, decimal_places=2)  # Ejemplo: 10.00 es 10%
    fecha_inicio = models.DateField()
    fecha_vencimiento = models.DateField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.codigo

    def esta_vigente(self):
        return self.activo and self.fecha_vencimiento >= datetime.date.today()


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_disponible = models.IntegerField()
    activo = models.BooleanField(default=True)
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)  # Nuevo campo de imagen

    def __str__(self):
        return self.nombre

class MenuDelDia(models.Model):
    fecha = models.DateField()
    productos = models.ManyToManyField(Producto, through='MenuProducto')

class MenuProducto(models.Model):
    menu = models.ForeignKey(MenuDelDia, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_disponible = models.IntegerField()

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('PREPARANDO', 'Preparando'),
        ('LISTO', 'Listo para entrega'),
        ('ASIGNADO', 'Asignado a repartidor'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
    ]
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Cliente'})
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='PENDIENTE')
    direccion_entrega = models.CharField(max_length=255)

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

class Repartidor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'rol': 'Repartidor'})
    estado_activado = models.BooleanField(default=False)

class Fidelizacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'rol': 'Cliente'})
    tipo = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    vencimiento = models.DateField()
