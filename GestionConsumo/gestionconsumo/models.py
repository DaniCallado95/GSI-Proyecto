from django.db import models
from django.utils import timezone

class Usuario(models.Model):
    
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE) 
    username = models.CharField(max_length=50,primary_key=True) 
    password = models.CharField(max_length=50)
    roll = models.CharField(max_length=10)
    created_date = models.DateTimeField(default=timezone.now)
    def __str__(self): 
        return self.username

class Empresa(models.Model):
    
    empresa = models.CharField(max_length=50,primary_key=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self): 
        return self.empresa

class Activos(models.Model):
    
    def __str__(self): 
        return self.activo

class Consumo(models.Model):
    
    def __str__(self): 
        return self.consumo