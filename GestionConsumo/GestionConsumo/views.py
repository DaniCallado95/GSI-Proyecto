from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Empresa, Usuario, Activo, Consumo
from .forms import EmpresaForm, AdminEmpresaForm
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.http import Http404
# Create your views here.

def index(request):
    num_empresas = Empresa.objects.count()

    empresa = 0
    if request.user.is_authenticated:
        empresa_pk = Usuario.objects.get(user=request.user.id)
        empresa = empresa_pk.id_empresa.pk

    return render(
        request, 
        'index.html', 
        {'num_empresas': num_empresas, 'empresa': empresa}
    )

def listar_empresas(request):
    num_empresas = Empresa.objects.count()
    listadoEmpresas = Empresa.objects.all()
    return render(
        request, 
        'listaEmpresas.html', 
        {'num_empresas': num_empresas,'empresas': listadoEmpresas}
    )

def empresa_new(request):
    form_empresa = EmpresaForm()
    form_user = AdminEmpresaForm()
    return render(request, 'empresa_edit.html', {'form_empresa': form_empresa, 'form_user': form_user})

def verifyRegister(request):
    if request.method == 'POST':
        form_empresa = EmpresaForm(request.POST)
        form_user = AdminEmpresaForm(request.POST)
        if form_empresa.is_valid() and form_user.is_valid():

            # Create user and save to the database
            user = User.objects.create_user(form_user.cleaned_data.get('user'), form_empresa.cleaned_data.get('email'), form_user.cleaned_data.get('contrasena'))
            user.save()

            # Assign user to auth group
            group = Group.objects.get(name='administrador')
            group.user_set.add(user) 


            empresa = form_empresa.save()

            usuarioApp = Usuario(user=user, id_empresa=empresa)
            usuarioApp.save()

            # Si el usuario se crea correctamente 
            if user is not None:
                # Hacemos el login manualmente
                login(request, user)
                # Y le redireccionamos a la portada
                return redirect('empresa_perfil', pk=empresa.pk)
                
        else:
            raise Http404

def empresa_perfil(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    return render(request, 'empresa_perfil.html', {'empresa': empresa})