# Generated by Django 2.2.7 on 2019-12-12 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GestionConsumo', '0002_usuario_contrasena'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='contrasena',
        ),
    ]