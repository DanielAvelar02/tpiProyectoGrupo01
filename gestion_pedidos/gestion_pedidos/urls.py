# gestion_pedidos/urls.py
from django.contrib import admin
from django.urls import path, include
from negocio import views as negocio_views

urlpatterns = [
    
    
    path('admin/', admin.site.urls), # ruta para el admin de Django
    path('accounts/login/', negocio_views.custom_login, name='login'), #ruta de inicio de sesion personalizado
    path('logout/', negocio_views.custom_logout, name='logout'),
    path('', negocio_views.inicio, name='inicio'),  # ruta para la página de inicio
    
    path('negocio/', include('negocio.urls')),
    path('admin-dashboard/', negocio_views.admin_dashboard, name='admin_dashboard'),  # Ruta para administración personalizada

]

