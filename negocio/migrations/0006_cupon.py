# Generated by Django 5.1.3 on 2024-12-07 18:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('negocio', '0005_alter_fidelizacion_usuario_alter_repartidor_usuario_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=50, unique=True)),
                ('descuento', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fecha_inicio', models.DateField()),
                ('fecha_vencimiento', models.DateField()),
                ('activo', models.BooleanField(default=True)),
                ('negocio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='negocio.negocio')),
            ],
        ),
    ]
