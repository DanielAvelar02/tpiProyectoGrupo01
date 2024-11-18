from django.shortcuts import render, redirect, get_object_or_404
from .models import Negocio, Producto #se importan los modelos
from .forms import EditarUsuarioForm, NegocioForm, CrearUsuarioForm #se importan los formularios
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group #uso el usuario de Django


#-------------------------------
#Daniel Avelar  INICIO
#-------------------------------
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
    return redirect('inicio')  # O cualquier página a la que desees redirigir

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
    negocio = Negocio.objects.first()  # Obtener el primer negocio (unico xD)
    
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
        'negocio': negocio 
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
        form = NegocioForm(request.POST, request.FILES, instance=negocio)
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

@login_required #valida que el usuario este logueado
@user_passes_test(es_encargado_menu) #valida que el usuario sea encargado de menu
def listar_productos(request):
    productos = Producto.objects.all()
    negocio = Negocio.objects.first()
    return render(request, 'producto/listar_productos.html', {'productos': productos, 'negocio': negocio})

@login_required
@user_passes_test(es_encargado_menu)
def crear_producto(request):
    negocio = Negocio.objects.first()  # Suponemos que solo hay un negocio
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        cantidad_disponible = request.POST.get('cantidad')
        negocio = Negocio.objects.first()
        if nombre and precio and cantidad_disponible is not None:
            try:
                precio = float(precio)
                cantidad_disponible = int(cantidad_disponible)
            except ValueError:
                return render(request, 'producto/crear_producto.html', {'negocio': negocio, 'error': 'El precio debe ser un número decimal y la cantidad debe ser un número entero'})
            producto = Producto(nombre=nombre, precio=precio, cantidad_disponible=cantidad_disponible, negocio=negocio)
            producto.save()
            return redirect('listar_productos')
        else:
            return render(request, 'producto/crear_producto.html', {'negocio': negocio, 'error': 'Faltan datos'})
    else:
        return render(request, 'producto/crear_producto.html', {'negocio': negocio})
        
def cambiar_estado_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.activo = not producto.activo
    producto.save()
    return redirect('listar_productos')

#-------------------------------
#Carlos Rauda Modificaciones FIN
#-------------------------------


#-------------------------------
#Benitez Modificaciones
#-------------------------------

from django.shortcuts import render

def menu_del_dia(request):
    # Aquí puedes obtener los platos del modelo si estuvieran definidos
    platos = [
        {"nombre": "Plato 1", "imagen": "https://via.placeholder.com/100"},
        {"nombre": "Plato 2", "imagen": "https://via.placeholder.com/100"},
        {"nombre": "Plato 3", "imagen": "https://via.placeholder.com/100"},
        {"nombre": "Plato 4", "imagen": "https://via.placeholder.com/100"},
        {"nombre": "Plato 5", "imagen": "https://via.placeholder.com/100"},
        {"nombre": "Plato 6", "imagen": "https://via.placeholder.com/100"},
    ]
    return render(request, 'cliente/menu_del_dia.html', {'platos': platos})

def ordenar_platillo(request, platillo_id):
    # Simulación de datos del platillo
    platillo = {
        'nombre': 'Hamburguesa Especial',
        'precio': 7.99,
        'imagen': 'https://via.placeholder.com/300',
        'incluye': [
            {'nombre': 'Papas', 'imagen': 'https://via.placeholder.com/50'},
            {'nombre': 'Soda', 'imagen': 'https://via.placeholder.com/50'},
            {'nombre': 'Hamburguesa', 'imagen': 'https://via.placeholder.com/50'}
        ]
    }
    return render(request, 'cliente/ordenar_platillo.html', {'platillo': platillo})

def pagar(request):
    return render(request, 'cliente/pago.html')

def seguimiento_pedido(request):
    return render(request, 'cliente/seguimiento_pedido.html')

