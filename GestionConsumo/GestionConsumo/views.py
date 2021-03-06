from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Empresa, Usuario, Activo, Consumo
from .forms import EmpresaForm, AdminEmpresaForm, ActivoForm, ConsumoForm
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.http import Http404
from django.views.decorators.csrf import csrf_protect
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import LineChart
from graphos.renderers.gchart import ColumnChart
from graphos.renderers.gchart import PieChart
from django.db.models import Sum
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

def empresa_activos_añadir(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    empresa_pk = 0
    form_activo = ActivoForm()
    if request.user.is_authenticated:
        usuario = Usuario.objects.get(user=request.user.id)
        empresa_pk = usuario.id_empresa.pk
        if int(pk)==int(empresa_pk):
            return render(request, 'empresa_activos_añadir.html', {'empresa': empresa, 'empresa_pk': empresa_pk, 'titulo': 'Añadir Activo', 'form_activo': form_activo})
        else:
            num_empresas = Empresa.objects.count()
            return render(request, 'index.html', {'num_empresas': num_empresas, 'empresa_pk': empresa_pk})

def verifyActivo(request, pk):
    if request.method == 'POST':
        form_activo = ActivoForm(request.POST)
        if form_activo.is_valid():
            datos = form_activo.cleaned_data
            empresa = Empresa.objects.get(pk = request.POST.get('id_empresa'))
            activo = Activo(id_empresa = empresa,nombre = datos.get("nombre"), descripcion = datos.get("descripcion"))
            activo.save()

            # Si el usuario se crea correctamente 
            if activo is not None:
                # Y le redireccionamos a la portada
                return redirect('empresa_activos', pk=empresa.pk)
                
        else:
            raise Http404

@csrf_protect
def deleteActivo(request, pk):
    if request.method == 'POST':
        id_activo = request.POST.get('id_activo')
        activo = Activo.objects.get(pk = id_activo)
        activo.delete()
        return redirect('empresa_activos', pk=pk)

def empresa_activos_editar(request, pk, id_activo):
    activo = get_object_or_404(Activo, pk=id_activo)
    data = {'pk': pk, 'id_empresa': activo.id_empresa, 'nombre': activo.nombre, 'descripcion': activo.descripcion}

    empresa = get_object_or_404(Empresa, pk=pk)
    empresa_pk = 0

    form_activo = ActivoForm(initial=data)

    if request.user.is_authenticated:
        usuario = Usuario.objects.get(user=request.user.id)
        empresa_pk = usuario.id_empresa.pk
        if int(pk)==int(empresa_pk):
            return render(request, 'empresa_activos_editar.html', {'empresa': empresa, 'empresa_pk': empresa_pk, 'titulo': 'Editar Activo', 'form_activo': form_activo})
        else:
            num_empresas = Empresa.objects.count()
            return render(request, 'index.html', {'num_empresas': num_empresas, 'empresa_pk': empresa_pk})

def editActivo(request, pk, id_activo):
    activo = get_object_or_404(Activo, pk=id_activo)
    if request.method == 'POST':
        form_activo = ActivoForm(request.POST)
        if form_activo.is_valid():
            datos = form_activo.cleaned_data
            empresa = Empresa.objects.get(pk = pk)
            activo.nombre = datos.get("nombre")
            activo.descripcion = datos.get("descripcion")
            activo.save()

            # Si el usuario se crea correctamente 
            if activo is not None:
                # Y le redireccionamos a la portada
                return redirect('empresa_activos', pk=empresa.pk)
                
        else:
            raise Http404
            
def empresa_consumos(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    empresa_pk = 0
    if request.user.is_authenticated:
        usuario = Usuario.objects.get(user=request.user.id)
        empresa_pk = usuario.id_empresa.pk
        consumos = []
        consumos = Consumo.objects.filter(id_empresa=empresa_pk)
        anos = Consumo.objects.filter(id_empresa=empresa_pk).values_list('año', flat=True).distinct().order_by('año')
        if int(pk)==int(empresa_pk):
            return render(request, 'empresa_consumos.html', {'empresa': empresa, 'empresa_pk': empresa_pk, 'titulo': 'Consumo', 'anos': anos})
        else:
            num_empresas = Empresa.objects.count()
            return render(request, 'index.html', {'num_empresas': num_empresas, 'empresa_pk': empresa_pk})

def empresa_consumos_añadir(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    empresa_pk = 0
    if request.user.is_authenticated:
        activos = []
        usuario = Usuario.objects.get(user=request.user.id)
        empresa_pk = usuario.id_empresa.pk
        activos = Activo.objects.filter(id_empresa=empresa_pk)
        # print(activos[1].id_activo)
        form_consumo = ConsumoForm(activos)
        if int(pk)==int(empresa_pk):
            return render(request, 'empresa_consumos_añadir.html', {'empresa': empresa, 'empresa_pk': empresa_pk, 'titulo': 'Añadir Consumo', 'form_consumo': form_consumo})
        else:
            num_empresas = Empresa.objects.count()
            return render(request, 'index.html', {'num_empresas': num_empresas, 'empresa_pk': empresa_pk})

def verifyConsumo(request, pk):
    if request.method == 'POST':
        activo = Activo.objects.get(pk=request.POST["activos"])
        empresa = Empresa.objects.get(pk = request.POST.get('id_empresa'))
        consumo = Consumo(id_empresa = empresa, id_activo = activo,año = request.POST["año"],tipo = request.POST["tipo"],consumo = request.POST["consumo"])
        consumo.co2_emitido = convertir(request.POST["tipo"],request.POST["consumo"])
        consumo.save()

        # Si el consumo se crea correctamente 
        if consumo is not None:
            # Y le redireccionamos a la portada
            return redirect('empresa_consumos', pk=empresa.pk)
            
    else:
        raise Http404

@csrf_protect
def deleteConsumo(request, pk):
    if request.method == 'POST':
        id_consumo = request.POST.get('id_consumo')
        consumo = Consumo.objects.get(pk = id_consumo)
        consumo.delete()
        return redirect('empresa_consumos', pk=pk)

def empresa_consumos_editar(request, pk, id_consumo):
    consumo = get_object_or_404(Consumo, pk=id_consumo)
    empresa = get_object_or_404(Empresa, pk=pk)
    empresa_pk = 0

    data = {'pk': pk, 'id_empresa': consumo.id_empresa, 'año': consumo.año,'tipo': consumo.tipo,'consumo': consumo.consumo}
    
    form_consumo = ConsumoForm(Activo.objects.filter(nombre=consumo.id_activo), initial=data)
    if request.user.is_authenticated:
        usuario = Usuario.objects.get(user=request.user.id)
        empresa_pk = usuario.id_empresa.pk
        if int(pk)==int(empresa_pk):
            return render(request, 'empresa_consumos_editar.html', {'empresa': empresa, 'empresa_pk': empresa_pk, 'titulo': 'Editar Consumo', 'form_consumo': form_consumo})
        else:
            num_empresas = Empresa.objects.count()
            return render(request, 'index.html', {'num_empresas': num_empresas, 'empresa_pk': empresa_pk})


def editConsumo(request, pk, id_consumo):
    if request.method == 'POST':
        consumo_borrar = Consumo.objects.get(pk=id_consumo)
        activo = Activo.objects.get(pk=request.POST["activos"])
        empresa = Empresa.objects.get(pk=pk)
        consumo = Consumo(id_empresa = empresa, id_activo = activo,año = request.POST["año"],tipo = request.POST["tipo"],consumo = request.POST["consumo"])
        consumo_borrar.delete()
        consumo.co2_emitido = convertir(request.POST["tipo"],request.POST["consumo"])
        consumo.save()

        # Si el consumo se crea correctamente 
        if consumo is not None:
            # Y le redireccionamos a la portada
            return redirect('empresa_consumos', pk=empresa.pk)
                
        else:
            raise Http404

def cargarAno(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    empresa_pk = 0
    if request.user.is_authenticated:
        request.GET['ano']
        usuario = Usuario.objects.get(user=request.user.id)
        empresa_pk = usuario.id_empresa.pk
        consumos = []
        consumos = Consumo.objects.filter(id_empresa=empresa_pk, año=request.GET['ano'])
        return render(request, 'consumos_anos.html', {'empresa_pk': empresa_pk, 'consumos': consumos})


def empresa_visualizacion(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    empresa_pk = 0
    if request.user.is_authenticated:
        usuario = Usuario.objects.get(user=request.user.id)
        empresa_pk = usuario.id_empresa.pk
        consumosPorAño = []
        consumosPorAño = Consumo.objects.filter(id_empresa=pk).values('año').annotate(consumo = Sum('consumo'))
        datosChart1 = [['Año','Consumo total']]
        for consumo in consumosPorAño:
            datosChart1.append([consumo['año'],int(consumo['consumo'])])
        consumosPorActivo = []
        consumosPorActivo = Consumo.objects.filter(id_empresa=pk).values('id_activo').annotate(consumo = Sum('consumo'))
        datosChart2 = [['Activo','Consumo total']]
        for consumo in consumosPorActivo:
            nombreActivo = Activo.objects.filter(pk=consumo['id_activo'])
            datosChart2.append([str(nombreActivo[0]),int(consumo['consumo'])])

        consumosPorTipo = []
        consumosPorTipo = Consumo.objects.filter(id_empresa=pk).values('tipo').annotate(consumo = Sum('consumo'))
        datosChart3 = [['Tipo','Consumo total']]
        for consumo in consumosPorTipo:
            datosChart3.append([str(consumo['tipo']),int(consumo['consumo'])])
        
        # DataSource object
        data_source1 = SimpleDataSource(data=datosChart1)
        data_source2 = SimpleDataSource(data=datosChart2)
        data_source3 = SimpleDataSource(data=datosChart3)
        # Chart object
        chart1 = ColumnChart(data_source1,options={'title':'Consumo total por año'})
        chart2 = PieChart(data_source2,options={'title':'Consumo total por activo'})
        chart3 = PieChart(data_source3,options={'title':'Consumo total por tipo'})
        return render(request, 'empresa_visualizacion.html', {'empresa': empresa, 'empresa_pk': empresa_pk, 'titulo': 'Graficos','chart1':chart1,'chart2':chart2, 'chart3':chart3})
        
    else:
        consumosPorAño = []
        consumosPorAño = Consumo.objects.filter(id_empresa=pk).values('año').annotate(consumo = Sum('consumo'))
        datosChart1 = [['Año','Consumo total']]
        for consumo in consumosPorAño:
            datosChart1.append([consumo['año'],int(consumo['consumo'])])
        consumosPorActivo = []
        consumosPorActivo = Consumo.objects.filter(id_empresa=pk).values('id_activo').annotate(consumo = Sum('consumo'))
        datosChart2 = [['Activo','Consumo total']]
        for consumo in consumosPorActivo:
            nombreActivo = Activo.objects.filter(pk=consumo['id_activo'])
            datosChart2.append([str(nombreActivo[0]),int(consumo['consumo'])])
        
        consumosPorTipo = []
        consumosPorTipo = Consumo.objects.filter(id_empresa=pk).values('tipo').annotate(consumo = Sum('consumo'))
        datosChart3 = [['Tipo','Consumo total']]
        for consumo in consumosPorTipo:
            datosChart3.append([str(consumo['tipo']),int(consumo['consumo'])])

        # DataSource object
        data_source1 = SimpleDataSource(data=datosChart1)
        data_source2 = SimpleDataSource(data=datosChart2)
        data_source3 = SimpleDataSource(data=datosChart3)
        # Chart object
        chart1 = ColumnChart(data_source1,options={'title':'Consumo total por año'})
        chart2 = PieChart(data_source2,options={'title':'Consumo total por activo'})
        chart3 = PieChart(data_source3,options={'title':'Consumo total por tipo'})
        return render(request, 'empresa_visualizacion.html', {'empresa': empresa, 'titulo': 'Graficos','chart1':chart1,'chart2':chart2, 'chart3':chart3})

def convertir(tipo, consumo):
    emision = dict()
    emision = {
            'ELECTRICIDAD': 0.5,
            'AGUA': 0.0,
            'GASOLINA': 1.5,
            'DIESEL': 3.0,
            'GAS': 2.0,       
    }
    co2 = emision[tipo]*float(consumo)
    return co2