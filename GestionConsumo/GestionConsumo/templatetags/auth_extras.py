from django import template
from django.contrib.auth.models import Group
from GestionConsumo.models import Empresa, Usuario, Activo, Consumo 

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name): 
    group = Group.objects.get(name=group_name) 
    return True if group in user.groups.all() else False

@register.filter(name='empresa')
def empresa(user, pk): 
    usuario = Usuario.objects.get(user=user.id)
    empresa_pk = usuario.id_empresa.pk 
    return True if int(pk)==int(empresa_pk) else False