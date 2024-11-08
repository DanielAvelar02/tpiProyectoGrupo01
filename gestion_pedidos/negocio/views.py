from django.http import HttpResponse

def home(request):
    return HttpResponse("Bienvenido a la página de inicio, el kuki <3")
