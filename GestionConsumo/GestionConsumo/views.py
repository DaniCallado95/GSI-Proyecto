from django.shortcuts import render
from .models import Empresa, Usuario, Activo, Consumo
from .forms import EmpresaForm
# Create your views here.

def index(request):
    num_empresas = Empresa.objects.count()
    return render(
        request, 
        'index.html', 
        {'num_empresas': num_empresas}
    )

def empresa_new(request):
    form = EmpresaForm()
    return render(request, 'empresa_edit.html', {'form': form})