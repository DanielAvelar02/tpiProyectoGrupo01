from django.core.management.base import BaseCommand
from app.models import Negocio, Usuario, Producto, Pedido, DetallePedido
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Crea datos de prueba para la base de datos"

    def handle(self, *args, **kwargs):
        # Crear un negocio
        negocio = Negocio.objects.create(
            nombre="Negocio Ejemplo",
            logo="logos/ejemplo.png",
            color_primario="#FF5733",
            color_secundario="#33FF57",
            color_terciario="#3357FF",
            slogan="Lo mejor para ti",
            programa_lealtad_activado=True,
            cupones_activado=True
        )

        # Crear un cliente
        user_cliente = User.objects.create_user(username="cliente1", password="password123")
        cliente = Usuario.objects.create(usuario=user_cliente, rol="Cliente", negocio=negocio)

        # Crear un repartidor
        user_repartidor = User.objects.create_user(username="repartidor1", password="password123")
        repartidor = Usuario.objects.create(usuario=user_repartidor, rol="Repartidor", negocio=negocio)

        # Crear productos
        producto1 = Producto.objects.create(nombre="Producto 1", precio=10.00, cantidad_disponible=100, activo=True, negocio=negocio)
        producto2 = Producto.objects.create(nombre="Producto 2", precio=20.00, cantidad_disponible=50, activo=True, negocio=negocio)

        # Crear un pedido
        pedido = Pedido.objects.create(
            cliente=cliente,
            total=50.00,
            estado="Pendiente",
            direccion_entrega="Calle Falsa 123"
        )

        # Agregar detalles del pedido
        DetallePedido.objects.create(pedido=pedido, producto=producto1, cantidad=2, precio_unitario=10.00)
        DetallePedido.objects.create(pedido=pedido, producto=producto2, cantidad=1, precio_unitario=20.00)

        # Mensaje de confirmación
        self.stdout.write(self.style.SUCCESS("Datos de prueba generados correctamente"))
