# negocio/urls.py
from django.urls import path
from . import views
from negocio import views as negocio_views

urlpatterns = [
    path('configurar-negocio/', views.negocio_config, name='configurar_negocio'),  # Configuración del negocio
    path('listar-usuarios/', views.listar_usuarios, name='listar_usuarios'),  # Listar usuarios
    path('crear-usuario/', views.crear_usuario, name='crear_usuario'),  # Crear usuario
    path('editar-usuario/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),  # Editar usuario
    path('eliminar-usuario/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),  # Eliminar usuario
    path('lealtad/', views.lealtad, name='lealtad'),  # Vista de lealtad
    
]
