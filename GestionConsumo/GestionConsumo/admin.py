from django.contrib import admin
from .models import Empresa, Usuario, Activo, Consumo

admin.site.register(Empresa)
admin.site.register(Usuario)
admin.site.register(Activo)
admin.site.register(Consumo)
