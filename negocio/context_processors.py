# negocio/context_processors.py
from .models import Negocio

#Agrega la variable negocio a todos los contextos de la aplicación
def negocio_context(request):
    negocio = Negocio.objects.first()  # Suponiendo que solo hay un negocio
    return {'negocio': negocio}

#NO BORRAR :>