from django import forms
from .models import Empresa, Usuario, Activo, Consumo

class EmpresaForm(forms.ModelForm):
    nombre = forms.CharField(label='Nombre de la empresa', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre de la empresa'}))
    email = forms.CharField(label='Correo de contacto de la empresa', widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Correo de contacto'}))
    telefono = forms.IntegerField(label='Teléfono de contacto la empresa', widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Teléfono de contacto'}))
    class Meta:
        model = Empresa
        fields = ('nombre', 'email', 'telefono', )

class AdminEmpresaForm(forms.Form):
    user = forms.CharField(label='Administrador de la empresa', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Introduzca aqui el nombre del administrador de la empresa'}))
    contrasena = forms.CharField(label='Contraseña del adminsitrador', widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Introduzca aqui la contraseña del administrador'}))
        