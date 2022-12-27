# Generated by Django 4.1.2 on 2022-11-07 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buscadorhorarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ruta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('json_data', models.JSONField(null=True)),
                ('slug', models.SlugField(allow_unicode=True, unique=True)),
                ('estacion_destino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='estacion_destino', to='buscadorhorarios.estacion')),
                ('estacion_origen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='estacion_origen', to='buscadorhorarios.estacion')),
            ],
            options={
                'verbose_name_plural': 'Rutas',
            },
        ),
    ]
