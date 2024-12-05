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


    path('listar-menus/', views.listar_menus, name='listar_menus'),
    path('crear-menu/', views.crear_menu, name='crear_menu'),
    path('editar-menu/', views.editar_menu, name='editar_menu'),
    path('historial-menus/', views.historial_menus, name='historial_menus'),
    path('eliminar-menu/<int:menu_id>/', views.eliminar_menu, name='eliminar_menu'),  # Ruta de eliminación



    #-------------------------------
    #Carlos Rauda Modificaciones FIN
    #-------------------------------



    #-------------------------------
    #Benitez Modificaciones
    #-------------------------------
    path('menu/', views.menu_del_dia, name='menu_del_dia'),
    path('ordenar-platillo/<int:platillo_id>/', views.ordenar_platillo, name='ordenar_platillo'),
    path('pagar/', views.pagar, name='pagar'),
    path('seguimiento-pedido/', views.seguimiento_pedido, name='seguimiento_pedido'),

    #Moises Modificaciones
    path('repartidor/pedidos/', views.pedidos_view, name='pedidos'),
    path('repartidor/historial_pedidos/', views.historial_pedidos, name='historial_pedidos'),

    #-------------------------------
    #Kenet Modificaciones INICIO
    #-------------------------------
    path('despacho_pedidos/', views.despacho_pedidos, name='despacho_pedidos'),
    path('despacho/actualizar/<int:pedido_id>/', views.actualizar_estado_pedido, name='actualizar_estado_pedido'),
    #-------------------------------
    #Kener Modificaciones FIN
    #-------------------------------


    #KIKE Modificaciones INICIO
    #-------------------------------
   path("asignacion_pedidos/", views.asignacion_pedidos, name="asignacion_pedidos"),
    #-------------------------------
    #KIKE Modificaciones FIN
    #-------------------------------

    
]
