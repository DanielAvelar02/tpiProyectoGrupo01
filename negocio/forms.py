from django import forms
from .models import Negocio, Producto, MenuDelDia, Reclamo
from django.contrib.auth.models import User, Group
from datetime import datetime, date


# Formulario para crear usuarios
class CrearUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),  # Incluye todos los grupos, incluso "Administrador"
        required=True,
        label="Grupo"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'grupo']
 
# Formulario para editar usuarios
class EditarUsuarioForm(forms.ModelForm):
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),  # Incluye todos los grupos, incluso "Administrador"
        required=True,
        label="Grupo"
    )
    
    new_password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label="Nueva Contraseña"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label="Confirmar Nueva Contraseña"
    )

    class Meta:
        model = User  # Usa el modelo User predeterminado
        fields = ['username', 'email', 'grupo']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si el usuario ya tiene un grupo, lo seleccionamos por defecto
        if self.instance.pk and self.instance.groups.exists():
            self.fields['grupo'].initial = self.instance.groups.first()
            
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        
        # Validar que ambas contraseñas coincidan si se proporciona una nueva contraseña
        if new_password or confirm_password:
            if new_password != confirm_password:
                self.add_error("confirm_password", "Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get("new_password")
        
        # Si se proporciona una nueva contraseña, actualizarla en el usuario
        if new_password:
            user.set_password(new_password)
        
        if commit:
            user.save()
            # Asignar el grupo después de guardar el usuario
            if self.cleaned_data["grupo"]:
                user.groups.set([self.cleaned_data["grupo"]])
        return user
  
# Formulario para configurar el negocio
class NegocioForm(forms.ModelForm):
    color_primario = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}), label="Color de Fondo")
    color_secundario = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}), label="Color de Textos")
    color_terciario = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}), label="Color Barra Navegacion")

    class Meta:
        model = Negocio
        fields = ['nombre', 'logo', 'color_primario', 'color_secundario', 'color_terciario', 'slogan', 'programa_lealtad_activado', 'cupones_activado']

#Formulario para crear clientes nuevos
class RegistrarClienteForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # Eliminamos el campo 'grupo'

    def save(self, commit=True):
        # Guardamos el usuario y asignamos el grupo "Cliente"
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Asignar el grupo "Cliente"
            cliente_group, created = Group.objects.get_or_create(name='Cliente')
            user.groups.add(cliente_group)
        return user

#Formulario para crear menus
class CrearMenuForm(forms.Form):
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        error_messages={'required': 'La fecha es obligatoria.'}
    )
    productos = forms.ModelMultipleChoiceField(
        queryset=Producto.objects.filter(activo=True),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        productos = Producto.objects.filter(activo=True)
        for producto in productos:
            self.fields[f'cantidad_{producto.id}'] = forms.IntegerField(
                required=False,
                min_value=1,
                max_value=producto.cantidad_disponible,
                widget=forms.NumberInput(attrs={'placeholder': f'Máx: {producto.cantidad_disponible}.'})
            )

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        productos = cleaned_data.get('productos')

        # Validar que la fecha no sea pasada
        if fecha and fecha < date.today():
            self.add_error('fecha', "No se pueden crear menús para fechas anteriores a la actual.")
        # Validar que no exista un menú para la fecha seleccionada
        elif fecha and MenuDelDia.objects.filter(fecha=fecha).exists():
            self.add_error('fecha', 'Ya existe un menú para esta fecha.')
        # Validar que al menos un producto haya sido seleccionado
        elif not productos:
            self.add_error('productos', "Debe seleccionar al menos un producto para el menú.")
                   
        # Validar cantidades asociadas a los productos seleccionados
        productos_con_cantidad = {}
        for producto in productos or []:  # Evitar errores si productos es None
            cantidad = cleaned_data.get(f'cantidad_{producto.id}')
            print(cantidad)
            if cantidad is not None:
                if cantidad > producto.cantidad_disponible:
                    self.add_error(f'cantidad_{producto.id}',
                                f'La cantidad para "{producto.nombre}" excede la disponible ({producto.cantidad_disponible}).')
                elif cantidad < 1:
                    self.add_error(f'cantidad_{producto.id}',
                                f'La cantidad para "{producto.nombre}" debe ser al menos 1.')
                else:
                    productos_con_cantidad[producto] = cantidad
             # Validación final: Verificar que haya al menos un producto con cantidad válida
            if not productos_con_cantidad and not self.errors.get('productos'):
                self.add_error('productos', "Debe especificar al menos una cantidad válida para los productos seleccionados.")

        # Agregar productos con cantidad válida al cleaned_data si todo es correcto
        cleaned_data['productos_con_cantidad'] = productos_con_cantidad

        return cleaned_data

class ReclamoForm(forms.ModelForm):
    class Meta:
        model = Reclamo
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
        labels = {
            'texto': 'Descripción del Reclamo',
        }