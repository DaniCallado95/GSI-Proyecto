from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Empresa, Usuario, Activo, Consumo
from .forms import *
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
    form2 = UsuarioEmpresaForm()
    return render(request, 'empresa_edit.html', {'form': form, 'form2': form2})

def verifyRegister(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        form2 = UsuarioEmpresaForm(request.POST)
        if form.is_valid() and form2.is_valid():
            # Create user and save to the database
            user = User.objects.create_user(form2.cleaned_data.get('user'), form.cleaned_data.get('email'), form2.cleaned_data.get('contrasena'))
            user.save()
            empresa = form.save()
            usuarioApp = Usuario(user=user, id_empresa=empresa)
            usuarioApp.save()
            print(form.cleaned_data.get('nombre'))
            print(form2.cleaned_data.get('user'))
        else:
            raise Http404
            
    return render(
        request, 
        'index.html', 
        {'num_empresas': 77}
    )