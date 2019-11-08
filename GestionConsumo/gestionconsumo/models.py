from django.db import models
from django.utils import timezone

class Usuario(models.Model):
    
    empresa = models.ForeignKey("empresa", on_delete=models.CASCADE) 
    username = models.CharField(max_length=50,primary_key=True) 
    password = models.CharField(max_length=50)
    roll = models.CharField(max_length=10)
    created_date = models.DateTimeField(default=timezone.now)
    def __str__(self): 
        return self.empresa
