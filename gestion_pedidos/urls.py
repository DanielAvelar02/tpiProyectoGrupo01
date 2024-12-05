# gestion_pedidos/urls.py
from django.contrib import admin
from django.urls import path, include
from negocio import views as negocio_views
from django.conf import settings # Importar la configuración de Django
from django.conf.urls.static import static # Importar la función para servir archivos multimedia

urlpatterns = [
    path('admin/', admin.site.urls), # Ruta de administrador de Django
    path('accounts/', include('django.contrib.auth.urls')),  # Asegúrate de incluir las URLs de autenticación
    path('accounts/login/', negocio_views.custom_login, name='login'), #Ruta para el login personalizado
    path('logout/', negocio_views.custom_logout, name='logout'), #Ruta para el logout personalizado
    path('', negocio_views.inicio, name='inicio'),  # Ruta de la vista de inicio
    path('negocio/', include('negocio.urls')), #Rutas de la app negocio
    path('registrar-cliente/', negocio_views.registrar_cliente, name='registrar_cliente'), #Ruta para registrar un cliente nuevo
    path('despacho_pedidos/', negocio_views.despacho_pedidos, name='despacho_pedidos'), #Ruta para despachar pedidos

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Ruta para servir archivos multimedia

