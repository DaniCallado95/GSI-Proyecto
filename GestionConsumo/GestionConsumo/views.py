from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Empresa, Usuario, Activo, Consumo
from .forms import EmpresaForm, AdminEmpresaForm
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.http import Http404
from django.views.decorators.csrf import csrf_protect
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
        {'num_empresas': num_empresas, 'empresa_pk': empresa}
    )

def empresa_listar(request):
    num_empresas = Empresa.objects.count()
    listadoEmpresas = Empresa.objects.all()

    empresa = 0
    if request.user.is_authenticated:
        empresa_pk = Usuario.objects.get(user=request.user.id)
        empresa = empresa_pk.id_empresa.pk

    return render(
        request, 
        'empresa_listar.html', 
        {'num_empresas': num_empresas,'empresas': listadoEmpresas, 'empresa_pk': empresa}
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

    empresa_pk = 0
    if request.user.is_authenticated:
        usuario = Usuario.objects.get(user=request.user.id)
        empresa_pk = usuario.id_empresa.pk

    return render(request, 'empresa_perfil.html', {'empresa': empresa, 'empresa_pk': empresa_pk})

def empresa_usuarios(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    empresa_pk = 0
    if request.user.is_authenticated:
        usuario = Usuario.objects.get(user=request.user.id)
        empresa_pk = usuario.id_empresa.pk
        usuarios = []
        usuarios = Usuario.objects.filter(id_empresa=empresa_pk).exclude(user = request.user)
        if int(pk)==int(empresa_pk):
            return render(request, 'empresa_usuarios.html', {'empresa': empresa, 'empresa_pk': empresa_pk, 'titulo': 'Usuarios', 'usuarios':usuarios})
        else:
            num_empresas = Empresa.objects.count()
            return render(request, 'index.html', {'num_empresas': num_empresas, 'empresa_pk': empresa_pk})


@csrf_protect
def empresa_add_user(request, pk):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        contrasena = request.POST.get('pass')
        empresa = request.POST.get('empresa_pk')
        # Create user and save to the database
        user = User.objects.create_user(usuario, '', contrasena)
        user.save()

        # Assign user to auth group
        group = Group.objects.get(name='editor')
        group.user_set.add(user) 

        empresa = Empresa.objects.get(id_empresa=pk)

        usuarioApp = Usuario(user=user, id_empresa=empresa)
        usuarioApp.save()

        # Si el usuario se crea correctamente 
        if user is not None:
            # Y le redireccionamos a la portada
            return redirect('empresa_usuarios', pk=pk)

@csrf_protect
def empresa_delete_user(request, pk):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        empresa = request.POST.get('empresa_pk')

        user = User.objects.get(username = usuario)

        usuario_empresa = Usuario.objects.get(user=user.id, id_empresa = pk)

        usuario_empresa.delete()
        user.delete()
        return redirect('empresa_usuarios', pk=pk)

def empresa_activos(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    empresa_pk = 0
    if request.user.is_authenticated:
        usuario = Usuario.objects.get(user=request.user.id)
        empresa_pk = usuario.id_empresa.pk
        activos = []
        activos = Activo.objects.filter(id_empresa=empresa_pk)
        if int(pk)==int(empresa_pk):
            return render(request, 'empresa_activos.html', {'empresa': empresa, 'empresa_pk': empresa_pk, 'titulo': 'Activos', 'activos': activos})
        else:
            num_empresas = Empresa.objects.count()
            return render(request, 'index.html', {'num_empresas': num_empresas, 'empresa_pk': empresa_pk})

def empresa_consumos(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    empresa_pk = 0
    if request.user.is_authenticated:
        usuario = Usuario.objects.get(user=request.user.id)
        empresa_pk = usuario.id_empresa.pk
        consumos = []
        #consumos = Consumo.objects.filter(id_empresa=empresa_pk)
        consumos = Consumo.objects.all()
        if int(pk)==int(empresa_pk):
            return render(request, 'empresa_consumos.html', {'empresa': empresa, 'empresa_pk': empresa_pk, 'titulo': 'Consumo', 'consumos': consumos})
        else:
            num_empresas = Empresa.objects.count()
            return render(request, 'index.html', {'num_empresas': num_empresas, 'empresa_pk': empresa_pk})




            