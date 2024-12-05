# gestion_pedidos/negocio/signals.py
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group
from django.dispatch import receiver

@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    # Define los nombres de los grupos (roles)
    groups = ["Administrador", "Encargado de Menú", "Encargado de Registro de Pedidos", "Despacho de Pedidos", "Repartidor", "Cliente"]
    
    for group_name in groups:
        Group.objects.get_or_create(name=group_name)
