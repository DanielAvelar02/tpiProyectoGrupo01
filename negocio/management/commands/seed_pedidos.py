from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from negocio.models import Pedido, DetallePedido, Producto, Negocio
from django.utils import timezone
from datetime import timedelta
import random
import os
from django.core.files import File

class Command(BaseCommand):
    help = 'Crea datos de prueba para la entidad Pedido'

    def handle(self, *args, **kwargs):
        # Crear negocio si no existe
        negocio, created = Negocio.objects.get_or_create(
            nombre="Restaurante Demo",
            defaults={
                'slogan': "La mejor comida",
                'color_primario': '#FFFFFF',
                'color_secundario': '#000000',
                'color_terciario': '#888888'
            }
        )

        if created:
            # Asignar una imagen predeterminada al logo
            logo_path = os.path.join(os.path.dirname(__file__), 'default_logo.png')
            with open(logo_path, 'rb') as logo_file:
                negocio.logo.save('default_logo.png', File(logo_file), save=True)

        # Crear productos de prueba si no existen
        productos_demo = [
            {'nombre': 'Hamburguesa Clásica', 'precio': 5.99},
            {'nombre': 'Pizza Margherita', 'precio': 8.99},
            {'nombre': 'Ensalada César', 'precio': 4.99},
            {'nombre': 'Tacos al Pastor', 'precio': 3.99},
            {'nombre': 'Sushi Roll', 'precio': 7.99}
        ]

        for producto_data in productos_demo:
            Producto.objects.get_or_create(
                nombre=producto_data['nombre'],
                defaults={
                    'precio': producto_data['precio'],
                    'cantidad_disponible': 50,
                    'negocio': negocio,
                    'activo': True
                }
            )

        # Asegúrate de tener al menos un cliente
        cliente_group, _ = Group.objects.get_or_create(name='Cliente')
        clientes = User.objects.filter(groups=cliente_group)
        
        if not clientes.exists():
            # Crear algunos clientes de prueba si no existen
            for i in range(1, 4):
                usuario = User.objects.create_user(
                    username=f'cliente{i}',
                    password='cliente123',
                    email=f'cliente{i}@example.com'
                )
                usuario.groups.add(cliente_group)
                clientes = User.objects.filter(groups=cliente_group)

        # Obtener productos existentes
        productos = list(Producto.objects.filter(activo=True))
        
        if not productos:
            self.stdout.write(self.style.ERROR('No hay productos activos en la base de datos'))
            return

        # Crear pedidos de prueba
        estados = ['PENDIENTE', 'PREPARANDO', 'LISTO', 'ASIGNADO', 'ENTREGADO']
        direcciones = [
            'Calle Principal #123',
            'Avenida Central #456',
            'Boulevard Norte #789',
            'Colonia Las Flores #321',
            'Residencial El Prado #654'
        ]

        # Crear 15 pedidos de prueba
        for i in range(15):
            # Calcular fecha aleatoria en las últimas 24 horas
            horas_aleatorias = random.randint(0, 24)
            fecha_pedido = timezone.now() - timedelta(hours=horas_aleatorias)
            
            # Crear el pedido
            pedido = Pedido.objects.create(
                cliente=random.choice(clientes),
                fecha_pedido=fecha_pedido,
                estado=random.choice(estados),
                direccion_entrega=random.choice(direcciones),
                total=0  # Se actualizará después
            )

            # Agregar productos aleatorios al pedido
            total_pedido = 0
            num_productos = random.randint(1, 4)
            productos_seleccionados = random.sample(productos, num_productos)

            for producto in productos_seleccionados:
                cantidad = random.randint(1, 3)
                precio_unitario = producto.precio
                subtotal = cantidad * precio_unitario

                DetallePedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario
                )
                total_pedido += subtotal

            # Actualizar el total del pedido
            pedido.total = total_pedido
            pedido.save()

        self.stdout.write(self.style.SUCCESS('Se crearon los datos de prueba exitosamente'))