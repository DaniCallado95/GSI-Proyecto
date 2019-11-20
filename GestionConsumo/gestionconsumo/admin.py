from django.contrib import admin
from .models import Empresa
from .models import Usuario
from .models import Activo
from .models import Consumo

admin.site.register(Empresa)
admin.site.register(Usuario)
admin.site.register(Activo)
admin.site.register(Consumo)
