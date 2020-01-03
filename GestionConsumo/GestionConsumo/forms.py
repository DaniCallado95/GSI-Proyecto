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
        
class ActivoForm(forms.Form):
    nombre = forms.CharField(label='Nombre del activo', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Introduzca aqui el nombre del activo'}))
    descripcion = forms.CharField(label='Descripcion del activo', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Introduzca aqui la descripcion del activo'}))
    
    class Meta:
        model = Activo
        fields = ('nombre', 'descripcion',)

class ConsumoForm(forms.Form):

    def __init__(self,activos,*args,**kwargs):
        super(ConsumoForm,self).__init__(*args,**kwargs)
        self.fields['activos'] = forms.ChoiceField(choices=tuple([(activos[x].id_activo, activos[x]) for x in range(len(activos))]))

    tipos = [('1', 'ELECTRICIDAD'), ('2', 'AGUA'),('2', 'GASOLINA'),('2', 'DIESEL'),('2', 'GAS')]

    año = forms.IntegerField(label='Año de consumo', widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Año de consumo'}))
    tipo = forms.ChoiceField(choices=tipos)
    
    consumo = forms.CharField(label='Consumo', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Introduzca aqui el consumo'}))
    co2_emitido = forms.CharField(label='CO2_emitido', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Introduzca aqui el co2_emitido'}))
    
    class Meta:
        model = Consumo
        fields = ('año','tipo','consumo','co2_emitido','activos')