# gestion_pedidos/negocio/signals.py
import os
from django.db.models.signals import pre_save, post_migrate
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.conf import settings
from .models import Negocio

@receiver(pre_save, sender=Negocio)
def delete_old_logo(sender, instance, **kwargs):
    # Obtener el negocio actual antes de guardar
    try:
        old_logo = sender.objects.get(pk=instance.pk).logo
    except sender.DoesNotExist:
        old_logo = None  # No hay negocio previo

    new_logo = instance.logo  # Nuevo logo que se está guardando

    # Comparar directamente los valores de las URL
    if old_logo and old_logo != new_logo:
        # Aquí no se necesita eliminar el archivo porque estamos usando URLs
        print(f"Cambiando logo de {old_logo} a {new_logo}")

@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    # Define los nombres de los grupos (roles)
    groups = ["Administrador", "Encargado de Menú", "Encargado de Registro de Pedidos", "Despacho de Pedidos", "Repartidor", "Cliente"]
    
    for group_name in groups:
        Group.objects.get_or_create(name=group_name)
