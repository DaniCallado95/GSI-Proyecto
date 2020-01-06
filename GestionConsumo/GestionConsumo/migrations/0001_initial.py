# Generated by Django 2.2.7 on 2020-01-06 17:58

import GestionConsumo.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activo',
            fields=[
                ('id_activo', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id_empresa', models.AutoField(max_length=50, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('telefono', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionConsumo.Empresa')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Consumo',
            fields=[
                ('id_consumo', models.AutoField(primary_key=True, serialize=False)),
                ('año', models.PositiveIntegerField(default=2020, validators=[django.core.validators.MinValueValidator(1984), GestionConsumo.models.max_value_current_year])),
                ('tipo', models.CharField(choices=[('ELECTRICIDAD', 'electricidad'), ('AGUA', 'agua'), ('GASOLINA', 'gasolina'), ('DIESEL', 'diesel'), ('GAS', 'gas')], default='ELECTRICIDAD', max_length=15)),
                ('consumo', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('co2_emitido', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('id_activo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionConsumo.Activo')),
                ('id_empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionConsumo.Empresa')),
            ],
        ),
        migrations.AddField(
            model_name='activo',
            name='id_empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionConsumo.Empresa'),
        ),
    ]
