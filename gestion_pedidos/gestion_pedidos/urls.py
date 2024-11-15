# gestion_pedidos/urls.py
from django.contrib import admin
from django.urls import path, include
from negocio import views as negocio_views

urlpatterns = [
    path('admin/', admin.site.urls), # Ruta de administrador de Django
    path('accounts/login/', negocio_views.custom_login, name='login'), #Ruta para el login personalizado
    path('logout/', negocio_views.custom_logout, name='logout'), #Ruta para el logout personalizado
    path('', negocio_views.inicio, name='inicio'),  # Ruta de la vista de inicio
    path('negocio/', include('negocio.urls')) #Rutas de la app negocio

]

