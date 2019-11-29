from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

roles = (
            ('ad', 'admin'),
            ('añ', 'añadir'),
            ('ed', 'editar')
    )

class Usuario(models.Model):

    # Vincula los empleados con un usuario de la bd
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    id_empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    rol = models.CharField(max_length=10, choices=roles, default='añ')
    created_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self): 
        return self.id_empresa

class Empresa(models.Model):
    
    id_empresa = models.AutoField(max_length=50,primary_key=True)
    nombre = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

    # Buscar validador
    telefono = models.PositiveIntegerField()

    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self): 
        return self.nombre

class Activo(models.Model):
    
    id_empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    id_activo = models.AutoField(primary_key=True)

    # Los definimos por tipos (ej: coches, programas, electricidad, ..)??
    nombre = models.CharField(max_length=50)

    descripcion = models.TextField(max_length=500)

    def __str__(self): 
        return self.descripcion

class Consumo(models.Model):
    
    id_empresa = models.ForeignKey("Activo", related_name="empresa", on_delete=models.CASCADE)
    id_activo = models.ForeignKey("Activo", related_name="activo", on_delete=models.CASCADE)
    año = models.PositiveIntegerField(default=current_year(), validators=[MinValueValidator(1984), max_value_current_year], primary_key=True)
    consumo = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self): 
        return self.consumo
