from django.shortcuts import render
from .models import Empresa, Usuario, Activo, Consumo
# Create your views here.

def index(request):
    num_empresas = Empresa.objects.count()
    return render(
        request, 
        'index.html', 
        {'num_empresas': num_empresas}
    )