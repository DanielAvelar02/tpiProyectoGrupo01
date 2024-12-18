from django.shortcuts import render, redirect, get_object_or_404
from .models import DetallePedido, Negocio, Producto, MenuDelDia, MenuProducto, Pedido #se importan los modelos
from .forms import EditarUsuarioForm, NegocioForm, CrearUsuarioForm, RegistrarClienteForm, CrearMenuForm #se importan los formularios
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group #uso el usuario de Django
from datetime import date
from django.contrib import messages
from .models import Reclamo
from .forms import ReclamoForm

#-------------------------------
#Daniel Avelar  INICIO
#-------------------------------
def custom_404(request, exception):
    return render(request, '404.html', status=404)

handler404 = custom_404

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('inicio')  # Redirige a la vista de inicio (ajusta según sea necesario)
            else:
                form.add_error(None, 'Usuario o contraseña incorrectos')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('/')  # O cualquier página a la que desees redirigir

# Vista de inicio, solo accesible si el usuario está logueado
@login_required
def inicio(request):
    # Inicializar variables
    es_administrador = es_encargado_menu = es_encargado_registro = es_despacho =es_cliente=es_repartidor = False
    nombre_usuario = ""
    tipo_usuario = "Sin grupo"

    # Verificar si el usuario está autenticado
    if request.user.is_authenticated:
        # Obtener el nombre del usuario
        nombre_usuario = request.user.get_full_name() or request.user.username

        # Obtener los grupos del usuario
        grupos_usuario = request.user.groups.values_list('name', flat=True)
        
        # Definir las variables para los grupos
        es_administrador = 'Administrador' in grupos_usuario
        es_encargado_menu = 'Encargado de Menú' in grupos_usuario
        es_encargado_registro = 'Encargado de Registro de Pedidos' in grupos_usuario
        es_despacho = 'Despacho de Pedidos' in grupos_usuario
        es_cliente= 'Cliente' in grupos_usuario
        es_repartidor = 'Repartidor' in grupos_usuario


        # Definir el tipo de usuario según su grupo principal
        if es_administrador:
            tipo_usuario = "Administrador"
        elif es_encargado_menu:
            tipo_usuario = "Encargado de Menú"
        elif es_encargado_registro:
            tipo_usuario = "Encargado de Registro de Pedidos"
        elif es_despacho:
            tipo_usuario = "Despacho de Pedidos"
        elif es_cliente:
            tipo_usuario = "Cliente"
        elif es_repartidor:
            tipo_usuario = "Repartidor"
        
    # Obtener datos del negocio
    try:
        negocio = Negocio.objects.first()
    except:
        negocio = None
    
    # Pasar las variables al contexto
    return render(request, 'inicio.html', {
        'es_administrador': es_administrador,
        'es_encargado_menu': es_encargado_menu,
        'es_encargado_registro': es_encargado_registro,
        'es_despacho': es_despacho,
        'es_cliente': es_cliente,
        'es_repartidor': es_repartidor,
        'nombre_usuario': nombre_usuario,
        'tipo_usuario': tipo_usuario,
        'negocio': negocio,
    })    
 
# Verificar si el usuario es Administrador
def es_administrador(user):
    return user.is_authenticated and user.groups.filter(name='Administrador').exists()
      
# Vista para la configuración del negocio (pendiente)
@login_required
@user_passes_test(es_administrador)
def negocio_config(request):
    negocio = Negocio.objects.first()  # Suponemos que solo hay un negocio
    if request.method == "POST":
        form = NegocioForm(request.POST, instance=negocio)
        if form.is_valid():
            form.save()
            return redirect('inicio')  # Redirige al inicio después de guardar
    else:
        form = NegocioForm(instance=negocio)
    return render(request, 'negocio/configurar_negocio.html', {'form': form})

# Vista para listar los usuarios
@login_required
@user_passes_test(es_administrador)
def listar_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'usuario/listar_usuarios.html', {'usuarios': usuarios})

# Vista para crear un nuevo usuario
@login_required
@user_passes_test(es_administrador)
def crear_usuario(request):
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            # Asignar el grupo al usuario
            usuario.groups.add(form.cleaned_data['grupo'])
            return redirect('listar_usuarios')
    else:
        form = CrearUsuarioForm()
    return render(request, 'usuario/crear_usuario.html', {'form': form})

# Vista para editar un usuario
@login_required
@user_passes_test(es_administrador)
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    es_unico_admin = usuario.groups.filter(name='Administrador').exists() and \
                     User.objects.filter(groups__name='Administrador').count() == 1

    if request.method == "POST":
        form = EditarUsuarioForm(request.POST, instance=usuario)
        
        # Verifica si es el único administrador e intenta cambiar su propio rol
        if es_unico_admin and request.user == usuario:
            # Excluye el campo 'grupo' para que no pueda modificar su rol
            form.fields.pop('grupo')

        if form.is_valid():
            form.save()
            
            # Asegura que el grupo se actualice al nuevo valor
            if form.cleaned_data.get('grupo'):
                usuario.groups.set([form.cleaned_data['grupo']])
                 
            # Si es el único admin y se está editando a sí mismo, asegura que se mantenga en el grupo 'Administrador'
            if es_unico_admin and request.user == usuario:
                admin_group = Group.objects.get(name='Administrador')
                usuario.groups.set([admin_group])
            return redirect('listar_usuarios')
    else:
        form = EditarUsuarioForm(instance=usuario)
        
        # Remueve el campo 'grupo' si es el único administrador editándose a sí mismo
        if es_unico_admin and request.user == usuario:
            form.fields.pop('grupo')

    return render(request, 'usuario/editar_usuario.html', {
        'form': form,
        'usuario': usuario,
        'es_unico_admin': es_unico_admin
    })
    
# Vista para eliminar un usuario
@login_required
@user_passes_test(es_administrador)
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    
    # Evitar que el administrador se elimine a sí mismo o eliminar el último administrador
    if usuario == request.user or usuario.groups.filter(name="Administrador").exists() and User.objects.filter(groups__name="Administrador").count() == 1:
        # Mostrar un mensaje de error o redirigir
        return redirect('listar_usuarios')  # Puedes añadir un mensaje para informar al usuario

    if request.method == "POST":
        usuario.delete()
        return redirect('listar_usuarios')
    return render(request, 'usuario/eliminar_usuario.html', {'usuario': usuario})

# Vista para listar los usuarios
@login_required
@user_passes_test(es_administrador)
def lealtad(request):
    return render(request, 'lealtad/lealtad.html', {})

#-------------------------------
#Vista para clientes

# Verificar si el usuario es Cliente
def es_cliente(user):
    return user.is_authenticated and user.groups.filter(name='Cliente').exists()

# Vista para registrar un cliente nuevo
def registrar_cliente(request):
    if request.method == 'POST':
        form = RegistrarClienteForm(request.POST)
        if form.is_valid():
             # Guardar el usuario y asignar automáticamente el grupo "Cliente"
            usuario = form.save()

            # Iniciar sesión automáticamente con el usuario recién creado
            login(request, usuario)

            return redirect('inicio')
    else:
        form = RegistrarClienteForm()
    return render(request, 'registration/registrar_cliente.html', {'form': form})
      

#-------------------------------
#Daniel Avelar  FIN
#-------------------------------


#-------------------------------
#Carlos Rauda Modificaciones INICIO
#-------------------------------

# Verificar si el usuario es Encargado de Menú
#Comentario daniel: se agrega la funcion es_encargado_menu para verificar si el usuario es encargado de menu
def es_encargado_menu(user):
    return user.is_authenticated and user.groups.filter(name='Encargado de Menú').exists()

def es_encargado_menu_and_es_cliente(user):
    return user.is_authenticated and user.groups.filter(name='Encargado de Menú').exists() or user.groups.filter(name='Cliente').exists()


@login_required #valida que el usuario este logueado
@user_passes_test(es_encargado_menu) #valida que el usuario sea encargado de menu
def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'producto/listar_productos.html', {'productos': productos})

@login_required
@user_passes_test(es_encargado_menu)
def crear_producto(request):
    accion = 'Agregar producto'
    action = '/negocio/crear-producto/'
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        cantidad_disponible = request.POST.get('cantidad')
        imagen = request.POST.get('imagen')  # Obtener la URL
        negocio = Negocio.objects.first()

        # Validar que no exista un producto con el mismo nombre
        if Producto.objects.filter(nombre=nombre).exists():
            return render(request, 'producto/crear_producto.html', {'accion': accion, 'action': action, 'error': 'Ya existe un producto con este nombre'})

        if nombre is not None and precio is not None and cantidad_disponible is not None:
            try:
                precio = float(precio)
                cantidad_disponible = int(cantidad_disponible)
            except ValueError:
                return render(request, 'producto/crear_producto.html', {
                    'accion': accion, 
                    'action': action,
                    'error': 'El precio debe ser un número decimal y la cantidad debe ser un número entero'
                })
            producto = Producto(
                nombre=nombre,
                precio=precio,
                cantidad_disponible=cantidad_disponible,
                imagen=imagen,# Guardar la URL
                negocio=negocio
            )            
            producto.save()
            return redirect('listar_productos')
        else:
            return render(request, 'producto/crear_producto.html', {'accion': accion, 'action': action, 'error': 'Faltan datos'})
    else:
        return render(request, 'producto/crear_producto.html', {'accion': accion, 'action': action})
        
def cambiar_estado_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.activo = not producto.activo
    producto.save()
    return redirect('listar_productos')

import os
from django.conf import settings

@login_required
@user_passes_test(es_encargado_menu)
def editar_producto(request, producto_id):
    accion = 'Guardar cambios'
    action = '/negocio/editar-producto/' + str(producto_id)
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        cantidad_disponible = request.POST.get('cantidad')
        imagen = request.POST.get('imagen')  # Obtener la URL

        
        # Validar que no exista un producto con el mismo nombre (excepto el actual)
        if Producto.objects.filter(nombre=nombre).exclude(id=producto_id).exists():
            return render(request, 'producto/crear_producto.html', {'producto': producto, 'accion': accion, 'action': action, 'error': 'Ya existe un producto con este nombre'})

        if nombre and precio and cantidad_disponible is not None:
            try:
                precio = float(precio)
                cantidad_disponible = int(cantidad_disponible)
            except ValueError:
                return render(request, 'producto/crear_producto.html', {'producto': producto, 'accion': accion, 'action': action, 'error': 'El precio debe ser un número decimal y la cantidad debe ser un número entero'})
            producto.nombre = nombre
            producto.precio = precio
            producto.cantidad_disponible = cantidad_disponible
            producto.imagen = imagen  # Guardar la URL actualizada

         
            producto.save()
            return redirect('listar_productos')
        else:
            return render(request, 'producto/crear_producto.html', {'error': 'Faltan datos', 'producto': producto, 'accion': accion, 'action': action})
    else:
        return render(request, 'producto/crear_producto.html', {'producto': producto, 'accion': accion, 'action': action})

@login_required
@user_passes_test(es_encargado_menu)
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if producto.imagen:
        if os.path.isfile(producto.imagen.path):
            os.remove(producto.imagen.path)
    producto.delete()
    return redirect('listar_productos')

#Modificaciones de Daniel a Carlo  INICIO

#Vista para crear el menú del día
@login_required
@user_passes_test(es_encargado_menu)
def crear_menu(request):
    if request.method == "POST":
        form = CrearMenuForm(request.POST)
        if form.is_valid():
            fecha = form.cleaned_data['fecha']
            productos_con_cantidad = form.cleaned_data['productos_con_cantidad']

            # Crear el menú
            menu = MenuDelDia.objects.create(fecha=fecha)
            for producto, cantidad in productos_con_cantidad.items():
                MenuProducto.objects.create(menu=menu, producto=producto, cantidad_disponible=cantidad)

            return redirect('listar_menus')

        # Renderizar con errores si el formulario no es válido
        return render(request, 'producto/crear_menu.html', {'form': form})

    # GET request
    form = CrearMenuForm()
    return render(request, 'producto/crear_menu.html', {'form': form})

# Vista para editar el menú del día
@login_required
@user_passes_test(es_encargado_menu)
def editar_menu(request):
    hoy = date.today()
    menu_hoy = MenuDelDia.objects.filter(fecha=hoy).first()

    if not menu_hoy:
        messages.error(request, "No hay menú para el día de hoy.")
        return redirect('listar_menus')
    
    productos_info = []
    productos_ids = []

    for producto in menu_hoy.productos.all():
        menu_producto = MenuProducto.objects.filter(menu=menu_hoy, producto=producto).first()
        if menu_producto:
            productos_info.append({
                'id': producto.id,
                'nombre': producto.nombre,
                'cantidad_disponible': menu_producto.cantidad_disponible
            })
            productos_ids.append(producto.id)  # Agregamos solo el ID

    if request.method == "POST":
        # Procesar la lógica de actualización del menú aquí
        productos_seleccionados = request.POST.getlist('productos')
        cantidades = request.POST.getlist('cantidades')

        try:
            # Limpiar relaciones anteriores
            menu_hoy.productos.clear()

            for producto_id, cantidad in zip(productos_seleccionados, cantidades):
                producto = Producto.objects.get(id=producto_id, activo=True)
                cantidad = int(cantidad)

                if cantidad > producto.cantidad_disponible:
                    messages.error(
                        request,
                        f'La cantidad de "{producto.nombre}" excede la disponible.'
                    )
                    return redirect('editar_menu')

                # Crear la relación actualizada
                MenuProducto.objects.create(menu=menu_hoy, producto=producto, cantidad_disponible=cantidad)

            messages.success(request, "El menú se actualizó correctamente.")
            return redirect('listar_menus')

        except (Producto.DoesNotExist, ValueError) as e:
            messages.error(request, "Ocurrió un error al actualizar el menú.")
            return redirect('editar_menu')
        
    return render(request, 'producto/editar_menu.html', {
        'menu': menu_hoy,
        'productos': Producto.objects.filter(activo=True),
        'productos_info': productos_info,
        'productos_ids': productos_ids
    })

# Vista para listar los menús
@login_required
# Disponible para Encargado de Menú y Cliente
def listar_menus(request):

     # Inicializar variables
    es_encargado_menu =es_cliente = False

    if request.user.is_authenticated:
        grupos_usuario = request.user.groups.values_list('name', flat=True)
        es_encargado_menu = 'Encargado de Menú' in grupos_usuario
        es_cliente= 'Cliente' in grupos_usuario

    hoy = date.today()
    menu_hoy = MenuDelDia.objects.filter(fecha=hoy).first()

    productos_info = []
    if menu_hoy:
        for producto in menu_hoy.productos.all():
            menu_producto = MenuProducto.objects.filter(menu=menu_hoy, producto=producto).first()
            if menu_producto:
                productos_info.append({
                    'nombre': producto.nombre,
                    'cantidad_disponible': menu_producto.cantidad_disponible
                })

    return render(request, 'producto/listar_menus.html', {
        'menu_hoy': {
            'fecha': hoy,
            'productos': productos_info
        },
        'es_encargado_menu': es_encargado_menu,
        'es_cliente': es_cliente,
    })

#Vista para ver el historial de menús
@login_required
@user_passes_test(es_encargado_menu)
def historial_menus(request):
    hoy = date.today()

    # Menús pasados (fecha menor a hoy)
    menus_pasados = MenuDelDia.objects.filter(fecha__lt=hoy).prefetch_related('menuproducto_set__producto').order_by('-fecha')

    # Menús futuros (fecha mayor o igual a hoy)
    menus_futuros = MenuDelDia.objects.filter(fecha__gte=hoy).prefetch_related('menuproducto_set__producto').order_by('fecha')

    return render(request, 'producto/historial_menus.html', {
        'menus_pasados': menus_pasados,
        'menus_futuros': menus_futuros,
    })



# Vista para eliminar un menú
@login_required
@user_passes_test(es_encargado_menu)
def eliminar_menu(request, menu_id):
    # Obtener el menú por su ID
    menu = get_object_or_404(MenuDelDia, id=menu_id)

    # Eliminar el menú
    menu.delete()

    # Mensaje de éxito
    messages.success(request, "El menú se ha eliminado correctamente.")

    # Redirigir al historial de menús
    return redirect('historial_menus')






#Modificaciones de Daniel a Carlo  FIN

#-------------------------------
#Carlos Rauda Modificaciones FIN
#-------------------------------


#-------------------------------
#Benitez Modificaciones
#-------------------------------

from django.shortcuts import render

@login_required
@user_passes_test(es_cliente)
def menu_del_dia(request):
    hoy = date.today()
    menu_hoy = MenuDelDia.objects.filter(fecha=hoy).first()
    productos_info = []

    if menu_hoy:
        for producto in menu_hoy.productos.all():
            menu_producto = MenuProducto.objects.filter(menu=menu_hoy, producto=producto).first()
            if menu_producto:
                productos_info.append({
                    'producto': producto,
                    'cantidad_disponible': menu_producto.cantidad_disponible
                })

    return render(request, 'cliente/menu_del_dia.html', {'productos_info': productos_info})

@login_required
@user_passes_test(es_cliente)
def agregar_al_carrito(request, producto_id):
    if request.method == 'POST':
        hoy = date.today()
        menu_hoy = MenuDelDia.objects.filter(fecha=hoy).first()
        print(menu_hoy) 
        producto = get_object_or_404(Producto, id=producto_id, activo=True)
        print(producto)
        menu_producto = get_object_or_404(MenuProducto, menu=menu_hoy, producto=producto)
        cantidad = int(request.POST.get('cantidad', 1))
        if cantidad > menu_producto.cantidad_disponible:
            messages.error(request, f'La cantidad de "{producto.nombre}" excede la disponible.')
            return redirect('menu_del_dia')

        carrito = request.session.get('carrito', {})
        if str(producto_id) in carrito:
            carrito[str(producto_id)] += cantidad
        else:
            carrito[str(producto_id)] = cantidad
        # Decrease the available quantity in MenuProducto and Producto
        menu_producto.cantidad_disponible -= cantidad
        menu_producto.save()
        producto.cantidad_disponible -= cantidad
        producto.save()
        request.session['carrito'] = carrito
        messages.success(request, f'Agregado {cantidad} de "{producto.nombre}" al carrito.')
        return redirect('menu_del_dia')


@login_required
@user_passes_test(es_cliente)
def cancelar_compra(request):
    hoy = date.today()
    menu_hoy = MenuDelDia.objects.filter(fecha=hoy).first()
    carrito = request.session.get('carrito', {})

    for producto_id, cantidad in carrito.items():
        producto = get_object_or_404(Producto, id=producto_id)
        menu_producto = get_object_or_404(MenuProducto, menu=menu_hoy, producto=producto)
        menu_producto.cantidad_disponible += cantidad
        menu_producto.save()
        producto.cantidad_disponible += cantidad
        producto.save()

    request.session['carrito'] = {}
    messages.success(request, 'Compra cancelada y carrito vaciado.')
    return redirect('menu_del_dia')

from django.shortcuts import render, get_object_or_404
from .models import Producto

def ordenar_platillo(request, platillo_id):
    platillo = get_object_or_404(Producto, id=platillo_id)
    hoy = date.today()
    menu_hoy = MenuDelDia.objects.filter(fecha=hoy).first()
    cantidad_disponible = 0

    if menu_hoy:
        menu_producto = MenuProducto.objects.filter(menu=menu_hoy, producto=platillo).first()
        if menu_producto:
            cantidad_disponible = menu_producto.cantidad_disponible

    return render(request, 'cliente/ordenar_platillo.html', {
        'platillo': platillo,
        'cantidad_disponible': cantidad_disponible
    })

@login_required
@user_passes_test(es_cliente)
def pagar(request):
    if request.method == 'POST':
        direccion = request.POST.get('direccion')
        carrito = request.session.get('carrito', {})
        
        if not direccion:
            messages.error(request, 'Por favor, ingrese una dirección.')
            return redirect('pago')

        # Crear el pedido
        pedido = Pedido.objects.create(
            cliente=request.user,
            direccion_entrega=direccion,
            total=sum(Producto.objects.get(id=producto_id).precio * cantidad for producto_id, cantidad in carrito.items())
        )

        # Crear los detalles del pedido
        for producto_id, cantidad in carrito.items():
            producto = get_object_or_404(Producto, id=producto_id)
            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=producto.precio
            )

        # Limpiar el carrito
        request.session['carrito'] = {}
        messages.success(request, 'Pedido realizado con éxito.')
        return redirect('listar_pedidos')

    return render(request, 'cliente/pago.html')

# Repartidor - Pedidos
def pedidos_view(request):
    pedidos = Pedido.objects.all().select_related('cliente')  # Seleccionar cliente para evitar consultas adicionales

    return render(request, 'repartidor/pedidos.html', {'pedidos': pedidos})

def historial_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'repartidor/historial_pedidos.html', {'pedidos': pedidos})

#-------------------------------
#Kenet Modificaciones INICIO
#-------------------------------

@login_required
def despacho_pedidos(request):
    # Obtener todos los pedidos que están en estado PENDIENTE o PREPARANDO
    pedidos = Pedido.objects.filter(
        estado__in=['PENDIENTE', 'PREPARANDO', 'LISTO']
    ).order_by('-fecha_pedido')
    
    return render(request, 'despacho/despachoDePedidos.html', {
        'pedidos': pedidos,
        'title': 'Despacho de Pedidos'
    })

@login_required
def actualizar_estado_pedido(request, pedido_id):
    if request.method == 'POST':
        try:
            pedido = get_object_or_404(Pedido, id=pedido_id)
            nuevo_estado = request.POST.get('nuevo_estado')
            if nuevo_estado in dict(Pedido.ESTADO_CHOICES):
                pedido.estado = nuevo_estado
                pedido.save()
                messages.success(request, f'Pedido #{pedido_id} actualizado a {nuevo_estado}')
            else:
                messages.error(request, 'Estado no válido')
        except Exception as e:
            messages.error(request, f'Error al actualizar el pedido: {str(e)}')
    return redirect('despacho_pedidos')

#-------------------------------
#Kener Modificaciones FIN
#-------------------------------

#-------------------------------
#KIKE Modificaciones INICIO
#-------------------------------
def asignacion_pedidos(request):
    pedidos = Pedido.objects.filter(estado="Pendiente")
    return render(request, "asignacion_pedidos.html", {"pedidos": pedidos})

#-------------------------------
#KIKE Modificaciones FIN
#-------------------------------
@login_required
@user_passes_test(es_cliente)
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    productos = Producto.objects.filter(id__in=carrito.keys())
    items_carrito = []
    carrito_vacio = True  # Variable para controlar si hay items

    for producto in productos:
        items_carrito.append({
            'producto': producto,
            'cantidad': carrito[str(producto.id)],
            'subtotal': producto.precio * carrito[str(producto.id)]
        })
    
    if items_carrito:
        carrito_vacio = False

    total = sum(item['subtotal'] for item in items_carrito)
    return render(request, 'cliente/ver_carrito.html', {
        'items_carrito': items_carrito, 
        'total': total,
        'carrito_vacio': carrito_vacio
    })

@login_required
@user_passes_test(es_cliente)
def listar_pedidos(request):
    pedidos = Pedido.objects.filter(cliente=request.user).order_by('-fecha_pedido')
    return render(request, 'cliente/listar_pedidos.html', {'pedidos': pedidos})

    return render(request, 'cliente/ver_carrito.html', {'items_carrito': items_carrito, 'total': total})

@login_required
@user_passes_test(es_cliente)
def realizar_reclamo(request):
    if request.method == 'POST':
        form = ReclamoForm(request.POST)
        if form.is_valid():
            reclamo = form.save(commit=False)
            reclamo.cliente = request.user
            reclamo.save()
            messages.success(request, 'Reclamo enviado con éxito.')
            return redirect('inicio')
    else:
        form = ReclamoForm()
    return render(request, 'cliente/reclamo.html', {'form': form})

@login_required
@user_passes_test(es_administrador)
def ver_reclamos(request):
    reclamos = Reclamo.objects.all().select_related('cliente')
    return render(request, 'negocio/ver_reclamos.html', {'reclamos': reclamos})
