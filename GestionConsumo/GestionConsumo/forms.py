from django import forms
from .models import Empresa, Usuario, Activo, Consumo

class EmpresaForm(forms.ModelForm):

    class Meta:
        model = Empresa
        fields = ('nombre', 'email', 'telefono', )