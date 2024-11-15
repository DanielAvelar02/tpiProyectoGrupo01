from django import forms
from .models import Negocio
from django.contrib.auth.models import User, Group

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
        
# Formulario para configurar el negocio
class NegocioForm(forms.ModelForm):
    class Meta:
        model = Negocio
        fields = ['nombre', 'logo', 'paleta_colores', 'slogan', 'programa_lealtad_activado', 'cupones_activado']
