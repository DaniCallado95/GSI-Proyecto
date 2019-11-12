from django.contrib import admin
from .models import Empresa
from .models import Usuario

admin.site.register(Empresa)
admin.site.register(Usuario)
