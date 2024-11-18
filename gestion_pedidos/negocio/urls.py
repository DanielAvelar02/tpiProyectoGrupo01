# negocio/urls.py
from django.urls import path
from . import views

urlpatterns = [
    #-------------------------------
    #Daniel Avelar  INICIO
    #-------------------------------
    path('configurar-negocio/', views.negocio_config, name='configurar_negocio'),  # Configuración del negocio
    path('listar-usuarios/', views.listar_usuarios, name='listar_usuarios'),  # Listar usuarios
    path('crear-usuario/', views.crear_usuario, name='crear_usuario'),  # Crear usuario
    path('editar-usuario/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),  # Editar usuario
    path('eliminar-usuario/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),  # Eliminar usuario
    path('lealtad/', views.lealtad, name='lealtad'),  # Vista de lealtad
    #-------------------------------
    #Daniel Avelar  FIN
    #-------------------------------
    
    
    #-------------------------------
    #Carlos Rauda Modificaciones INICIO
    #-------------------------------
    path('listar-productos/', views.listar_productos, name='listar_productos'),
    path('crear-producto/', views.crear_producto, name='crear_producto'),
    path('editar-producto/<int:producto_id>', views.editar_producto, name='editar_producto'),
    path('eliminar-producto/<int:producto_id>', views.eliminar_producto, name='eliminar_producto'),
    path('cambiar-estado-producto/<int:producto_id>/', views.cambiar_estado_producto, name='cambiar_estado_producto'),
    #-------------------------------
    #Carlos Rauda Modificaciones FIN
    #-------------------------------
]
