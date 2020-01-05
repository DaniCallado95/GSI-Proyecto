from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^empresa/listar/$', views.empresa_listar, name='empresa_listar'),
    url(r'^empresa/new/$', views.empresa_new, name='empresa_new'),
    url(r'^empresa/new/verifyRegister$', views.verifyRegister, name='verifyRegister'),
    url(r'^empresa/(?P<pk>\d+)/perfil$', views.empresa_perfil, name='empresa_perfil'),
    url(r'^empresa/(?P<pk>\d+)/usuarios/$', views.empresa_usuarios, name='empresa_usuarios'),
    url(r'^empresa/(?P<pk>\d+)/usuarios/addUser$', views.empresa_add_user, name='empresa_add_user'),
    url(r'^empresa/(?P<pk>\d+)/usuarios/deleteUser$', views.empresa_delete_user, name='empresa_delete_user'),
    url(r'^empresa/(?P<pk>\d+)/activos/$', views.empresa_activos, name='empresa_activos'),
    url(r'^empresa/(?P<pk>\d+)/activos/añadir/$', views.empresa_activos_añadir, name='empresa_activos_añadir'),
    url(r'^empresa/(?P<pk>\d+)/activos/añadir/verifyActivo$', views.verifyActivo, name='verifyActivo'),
    url(r'^empresa/(?P<pk>\d+)/activos/deleteActivo$', views.deleteActivo, name='deleteActivo'),
    url(r'^empresa/(?P<pk>\d+)/activos/(?P<id_activo>\d+)/editar/$', views.empresa_activos_editar, name='empresa_activos_editar'),
    url(r'^empresa/(?P<pk>\d+)/activos/(?P<id_activo>\d+)/editar/editActivo$', views.editActivo, name='editActivo'),
    url(r'^empresa/(?P<pk>\d+)/consumos/$', views.empresa_consumos, name='empresa_consumos'),
    url(r'^empresa/(?P<pk>\d+)/consumos/añadir/$', views.empresa_consumos_añadir, name='empresa_consumos_añadir'),
    url(r'^empresa/(?P<pk>\d+)/consumos/añadir/verifyConsumo$', views.verifyConsumo, name='verifyConsumo'),
    url(r'^empresa/(?P<pk>\d+)/consumos/deleteConsumo$', views.deleteConsumo, name='deleteConsumo'),
    url(r'^empresa/(?P<pk>\d+)/consumos/(?P<id_consumo>\d+)/editar/$', views.empresa_consumos_editar, name='empresa_consumos_editar'),
    url(r'^empresa/(?P<pk>\d+)/consumos/(?P<id_consumo>\d+)/editar/editConsumo$', views.editConsumo, name='editConsumo'),
    url(r'^empresa/(?P<pk>\d+)/consumos/cargarAno/$', views.cargarAno, name='cargarAno'),
    url(r'^empresa/(?P<pk>\d+)/visualizacion$', views.empresa_visualizacion, name='empresa_visualizacion'),
]