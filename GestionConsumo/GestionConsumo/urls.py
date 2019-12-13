from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^empresa/listar/$', views.empresa_listar, name='empresa_listar'),
    url(r'^empresa/new/$', views.empresa_new, name='empresa_new'),
    url(r'^empresa/new/verifyRegister$', views.verifyRegister, name='verifyRegister'),
    url(r'^empresa/(?P<pk>\d+)/perfil$', views.empresa_perfil, name='empresa_perfil'),
]