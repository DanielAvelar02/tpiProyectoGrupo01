# gestion_pedidos/negocio/signals.py
import os
from django.db.models.signals import pre_save, post_migrate
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.conf import settings
from .models import Negocio

@receiver(pre_save, sender=Negocio)
def delete_old_logo(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_logo = Negocio.objects.get(pk=instance.pk).logo
        except Negocio.DoesNotExist:
            return
        else:
            new_logo = instance.logo
            if old_logo and old_logo.url != new_logo.url:
                if os.path.isfile(old_logo.path):
                    os.remove(old_logo.path)

@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    # Define los nombres de los grupos (roles)
    groups = ["Administrador", "Encargado de Menú", "Encargado de Registro de Pedidos", "Despacho de Pedidos", "Repartidor", "Cliente"]
    
    for group_name in groups:
        Group.objects.get_or_create(name=group_name)
